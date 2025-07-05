from rest_framework_mongoengine.viewsets import ModelViewSet
from .models import PHQ9Assessment
from .serializers import PHQ9AssessmentSerializer

class PHQ9AssessmentViewSet(ModelViewSet):
    serializer_class = PHQ9AssessmentSerializer
    
    def get_queryset(self):
        return PHQ9Assessment.objects.all()