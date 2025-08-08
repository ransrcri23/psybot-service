#!/usr/bin/env python3
"""
Sistema de Documentación Automática
==================================
Script que analiza cambios de git usando Gemini AI y actualiza el wiki automáticamente.

Flujo:
1. Obtiene información del último commit
2. Analiza los cambios con Gemini AI (máximo 300 caracteres)
3. Actualiza el archivo logs.qmd en el wiki
"""

import os
import sys
import subprocess
import json
from datetime import datetime
from pathlib import Path
import re

# Rutas importantes
SOURCE_CODE_PATH = Path(__file__).parent
WIKI_PATH = Path(r"C:\Users\sanch\Projects\DEV\Cenfotec\BE\Quarto\quarto_construccion_mantenimiento")
LOGS_FILE = WIKI_PATH / "reto7" / "logs.qmd"

# Sistema configurado para trabajar solo con remoto 'personal'

def get_git_info():
    """
    Obtiene información del último commit
    """
    try:
        # Obtener hash del commit
        commit_hash = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], 
            cwd=SOURCE_CODE_PATH,
            text=True
        ).strip()
        
        # Obtener autor del commit
        commit_author = subprocess.check_output(
            ["git", "log", "-1", "--pretty=format:%an", commit_hash],
            cwd=SOURCE_CODE_PATH,
            text=True
        ).strip()
        
        # Obtener mensaje del commit
        commit_message = subprocess.check_output(
            ["git", "log", "-1", "--pretty=format:%s", commit_hash],
            cwd=SOURCE_CODE_PATH,
            text=True
        ).strip()
        
        # Obtener archivos modificados
        try:
            changed_files_output = subprocess.check_output(
                ["git", "diff", "--name-only", "HEAD~1", "HEAD"],
                cwd=SOURCE_CODE_PATH,
                text=True
            ).strip()
            changed_files = changed_files_output.split('\n') if changed_files_output else []
        except subprocess.CalledProcessError:
            # Si es el primer commit, comparar con árbol vacío
            changed_files_output = subprocess.check_output(
                ["git", "ls-files"],
                cwd=SOURCE_CODE_PATH,
                text=True
            ).strip()
            changed_files = changed_files_output.split('\n') if changed_files_output else []
        
        # Obtener diff detallado
        try:
            diff_content = subprocess.check_output(
                ["git", "diff", "HEAD~1", "HEAD"],
                cwd=SOURCE_CODE_PATH,
                text=True,
                encoding='utf-8',
                errors='replace'
            ).strip()
        except subprocess.CalledProcessError:
            # Si es el primer commit
            diff_content = f"Primer commit con archivos: {', '.join(changed_files[:5])}"
        
        return {
            "commit_hash": commit_hash[:7],  # Short hash
            "commit_message": commit_message,
            "author": commit_author,
            "changed_files": changed_files,
            "diff_content": diff_content,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    except subprocess.CalledProcessError as e:
        print(f"Error obteniendo información de git: {e}")
        return None

def analyze_changes_with_gemini(git_info):
    """
    Analiza los cambios usando Gemini AI con límite de 300 caracteres
    """
    try:
        # Configurar Django antes de importar
        sys.path.append(str(SOURCE_CODE_PATH))
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'psybot.settings')
        import django
        django.setup()
        
        # Importar el cliente de Gemini del proyecto
        from psybot.utils.gemini_client import gemini_client
        
        # Preparar el prompt para Gemini
        prompt = f"""
        Analiza los siguientes cambios de código y proporciona una descripción técnica MÁXIMO 300 caracteres:

        COMMIT: {git_info['commit_message']}
        ARCHIVOS MODIFICADOS: {', '.join(git_info['changed_files'][:5])}
        
        DIFERENCIAS:
        {git_info['diff_content'][:1500]}

        Requisitos:
        - Descripción técnica concisa
        - MÁXIMO 300 caracteres
        - Sin encabezados ni formato adicional
        - Explica qué se cambió y por qué
        """
        
        # Llamar a Gemini
        description = gemini_client.generate_text(prompt)
        
        if description:
            # Limpiar y formatear la respuesta
            description = description.strip()
            # Remover saltos de línea múltiples y formatear para tabla markdown
            description = re.sub(r'\n+', ' ', description)
            description = description.replace('|', '\\|')  # Escapar pipes para markdown
            
            # Limitar estrictamente a 300 caracteres
            if len(description) > 300:
                description = description[:297] + "..."
            
            return description
        else:
            # Fallback si Gemini falla
            fallback = f"Cambios en: {', '.join(git_info['changed_files'][:3])}"
            if len(fallback) > 300:
                fallback = fallback[:297] + "..."
            return fallback
            
    except Exception as e:
        print(f"Error analizando con Gemini: {e}")
        # Fallback: descripción básica
        fallback = f"Cambios en: {', '.join(git_info['changed_files'][:3])}"
        if len(fallback) > 300:
            fallback = fallback[:297] + "..."
        return fallback

def update_wiki_logs(git_info, ai_description):
    """
    Actualiza el archivo logs.qmd en el wiki
    """
    try:
        # Verificar que el archivo del wiki existe
        if not LOGS_FILE.exists():
            print(f"Error: No se encontró el archivo del wiki en {LOGS_FILE}")
            return False
        
        # Leer el archivo actual
        with open(LOGS_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Preparar la nueva fila
        new_row = f"|{git_info['commit_hash']}|{git_info['author']}|{ai_description}|{git_info['timestamp']}|"
        
        # Procesar líneas del archivo
        lines = content.split('\n')
        
        # Encontrar dónde insertar la nueva fila
        header_found = False
        separator_found = False
        insert_index = -1
        
        for i, line in enumerate(lines):
            if '| Commit' in line and 'Owner' in line:
                header_found = True
            elif header_found and line.startswith('|--'):
                separator_found = True
            elif header_found and separator_found:
                # Si encontramos la línea de ejemplo, la reemplazamos
                if line.strip() == '|abc|asd|asd|aaaa|':
                    lines[i] = new_row
                    insert_index = i
                    break
                # Si no hay línea de ejemplo, insertamos después del separador
                elif not line.strip().startswith('|') or line.strip() == '':
                    lines.insert(i, new_row)
                    insert_index = i
                    break
        
        # Si no encontramos dónde insertar, agregamos al final
        if insert_index == -1:
            lines.append(new_row)
        
        # Escribir el archivo actualizado
        updated_content = '\n'.join(lines)
        with open(LOGS_FILE, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"Wiki actualizado exitosamente: {LOGS_FILE}")
        
        # Hacer commit y push automático del wiki
        wiki_commit_success = commit_and_push_wiki_changes(git_info)
        
        return True
        
    except Exception as e:
        print(f"Error actualizando el wiki: {e}")
        return False

def commit_and_push_wiki_changes(git_info):
    """
    Hace commit y push automático de los cambios en el repositorio del wiki
    Flujo: quarto render → git add . → git commit → git push
    """
    try:
        print("Procesando wiki: quarto render + git commit + push...")
        
        # Cambiar al directorio del wiki
        wiki_dir = WIKI_PATH
        
        # Paso 1: Ejecutar quarto render
        print("   Ejecutando quarto render...")
        subprocess.run(
            ["quarto", "render"],
            cwd=wiki_dir,
            check=True,
            capture_output=True
        )
        
        # Paso 2: Agregar todos los archivos (incluyendo los generados)
        print("   Agregando archivos con git add .")
        subprocess.run(
            ["git", "add", "."],
            cwd=wiki_dir,
            check=True,
            capture_output=True
        )
        
        # Paso 3: Crear mensaje de commit descriptivo
        commit_message = f"Documentación automática: {git_info['commit_hash']} por {git_info['author']}"
        
        # Paso 4: Hacer commit
        print("   Haciendo commit...")
        subprocess.run(
            ["git", "commit", "-m", commit_message],
            cwd=wiki_dir,
            check=True,
            capture_output=True
        )
        
        # Paso 5: Hacer push al repositorio del wiki
        print("   Haciendo push...")
        subprocess.run(
            ["git", "push"],
            cwd=wiki_dir,
            check=True,
            capture_output=True
        )
        
        print(f"Wiki procesado y pusheado exitosamente: {commit_message}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Error en procesamiento del wiki: {e}")
        # Intentar mostrar el stderr si está disponible
        if hasattr(e, 'stderr') and e.stderr:
            print(f"Error details: {e.stderr.decode('utf-8', errors='replace')}")
        return False
    except Exception as e:
        print(f"Error inesperado en wiki: {e}")
        return False

def main():
    """
    Función principal
    """
    print("Iniciando sistema de documentación automática...")
    
    # Paso 1: Obtener información del git
    print("Obteniendo información del commit...")
    git_info = get_git_info()
    if not git_info:
        print("No se pudo obtener información del git")
        sys.exit(1)
    
    print(f"   Commit: {git_info['commit_hash']}")
    print(f"   Autor: {git_info['author']}")
    print(f"   Archivos: {len(git_info['changed_files'])} archivos modificados")
    
    # Paso 2: Analizar con Gemini
    print("Analizando cambios con Gemini AI...")
    ai_description = analyze_changes_with_gemini(git_info)
    print(f"   Descripción ({len(ai_description)} chars): {ai_description[:50]}...")
    
    # Paso 3: Actualizar wiki
    print("Actualizando wiki...")
    success = update_wiki_logs(git_info, ai_description)
    
    if success:
        print("Documentación automática completada exitosamente!")
        print(f"   Nueva entrada agregada al wiki: {git_info['commit_hash']} por {git_info['author']}")
    else:
        print("Error en la documentación automática")
        sys.exit(1)

if __name__ == "__main__":
    main()
