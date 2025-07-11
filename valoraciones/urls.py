from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import PHQ9AssessmentViewSet, analyze_phq9_with_gemini, analyze_multiple_phq9_trends

router = DefaultRouter()
router.register(r'assessments', PHQ9AssessmentViewSet, basename='phq9assessment')

# Rutas específicas primero (antes del router)
urlpatterns = [
    path('assessments/analyze/', analyze_phq9_with_gemini, name='analyze_phq9_with_gemini'),
    path('assessments/trends/', analyze_multiple_phq9_trends, name='analyze_multiple_phq9_trends'),
]

# Luego las rutas del router
urlpatterns += router.urls
