from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, AppointmentViewSet, TestResultViewSet, MedicationViewSet

# from .views import patient_list


# urlpatterns = [
    # path('', include(router.urls)),
#     path('list/', patient_list),
# ]



router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'appointments', AppointmentViewSet, basename='appointment')
router.register(r'test-results', TestResultViewSet, basename='test-result')
router.register(r'medications', MedicationViewSet, basename='medication')
urlpatterns = router.urls
