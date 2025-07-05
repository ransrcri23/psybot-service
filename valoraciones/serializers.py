from rest_framework_mongoengine.serializers import DocumentSerializer
from .models import PHQ9Assessment

class PHQ9AssessmentSerializer(DocumentSerializer):
    class Meta:
        model = PHQ9Assessment
        fields = ['patient_id', 'responses', 'date_created']