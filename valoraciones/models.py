from mongoengine import Document, UUIDField, ListField, IntField, DateTimeField, ValidationError
import uuid
from datetime import datetime

class PHQ9Assessment(Document):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    patient_id = UUIDField(required=True)
    responses = ListField(IntField(min_value=0, max_value=3), required=True)
    total_score = IntField()
    date_created = DateTimeField(default=datetime.utcnow)

    meta = {
        'indexes': ['patient_id'],
        'collection': 'phq9_assessment'
    }

    def validate(self, clean=True):
        # Validar que las respuestas sean exactamente 9
        if len(self.responses) != 9:
            raise ValidationError('PHQ-9 debe tener exactamente 9 respuestas')
        
        # Validar que el paciente existe
        from pacientes.models import Paciente
        if not Paciente.objects(id=self.patient_id).first():
            raise ValidationError('El paciente especificado no existe')
        
        super().validate(clean)

    def save(self, *args, **kwargs):
        # Calcular total_score automáticamente
        self.total_score = sum(self.responses)
        super().save(*args, **kwargs)