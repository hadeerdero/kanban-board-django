from rest_framework.routers import DefaultRouter
from .views import StageViewSet, LeadViewSet

router = DefaultRouter()
router.register('stages', StageViewSet)
router.register('leads', LeadViewSet)

urlpatterns = router.urls
