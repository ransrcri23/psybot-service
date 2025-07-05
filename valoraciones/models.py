from mongoengine import Document, UUIDField, ListField, IntField, DateTimeField
import uuid
from datetime import datetime


class PHQ9Assessment(Document):
    patient_id = UUIDField(required=True)
    responses = ListField(IntField(min_value=0, max_value=3), required=True)
    total_score = IntField() 
    date_created = DateTimeField(default=datetime.utcnow)

    meta = {
        'indexes': ['patient_id']
    }

    def save(self, *args, **kwargs):
        self.total_score = sum(self.responses)
        super().save(*args, **kwargs)