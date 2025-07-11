from rest_framework_mongoengine.viewsets import ModelViewSet
from .models import Paciente
from .serializers import PacienteSerializer

class PacienteViewSet(ModelViewSet):
    serializer_class = PacienteSerializer
    
    def get_queryset(self):
        return Paciente.objects.all()