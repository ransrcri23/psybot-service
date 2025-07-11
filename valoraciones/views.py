from rest_framework_mongoengine.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import PHQ9Assessment
from .serializers import PHQ9AssessmentSerializer

class PHQ9AssessmentViewSet(ModelViewSet):
    serializer_class = PHQ9AssessmentSerializer
    
    def get_queryset(self):
        return PHQ9Assessment.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(
                    {'error': str(e)}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)