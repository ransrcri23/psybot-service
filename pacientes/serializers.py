from rest_framework_mongoengine.serializers import DocumentSerializer
from .models import Paciente

class PacienteSerializer(DocumentSerializer):
    class Meta:
        model = Paciente
        fields = ['id', 'nombre', 'apellido', 'identificacion', 'fecha_nacimiento', 'fecha_creacion']
        read_only_fields = ['id', 'fecha_creacion']