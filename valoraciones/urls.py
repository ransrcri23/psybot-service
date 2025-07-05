from rest_framework.routers import DefaultRouter
from .views import PHQ9AssessmentViewSet

router = DefaultRouter()
router.register(r'assessments', PHQ9AssessmentViewSet, basename='phq9assessment')

urlpatterns = router.urls