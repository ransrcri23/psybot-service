from rest_framework_mongoengine.viewsets import ModelViewSet
from .models import User
from .serializers import UserSerializer

class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    
    def get_queryset(self):
        return User.objects.all()
