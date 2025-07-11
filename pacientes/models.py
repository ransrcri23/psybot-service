from mongoengine import Document, StringField, DateField, DateTimeField, UUIDField
import uuid
from datetime import datetime

class Paciente(Document):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    nombre = StringField(required=True, max_length=100)
    apellido = StringField(required=True, max_length=100)
    identificacion = StringField(required=True, unique=True, max_length=20)
    fecha_nacimiento = DateField(required=True)
    fecha_creacion = DateTimeField(default=datetime.now)

    meta = {
        'indexes': ['identificacion'],
        'collection': 'pacientes'
    }

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.identificacion}"