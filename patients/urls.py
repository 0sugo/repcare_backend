from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, AppointmentViewSet, TestResultViewSet, MedicationViewSet



router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'appointments', AppointmentViewSet, basename='appointment')
router.register(r'test-results', TestResultViewSet, basename='test-result')
router.register(r'medications', MedicationViewSet, basename='medication')
urlpatterns = router.urls

# Patients:
# GET /api/patients/ - List all patients (for current user)
# GET /api/patients/dashboard_metrics/ - Get dashboard metrics
# POST /api/patients/ - Create patient profile
# GET /api/patients/{id}/ - Get specific patient
# PUT /api/patients/{id}/ - Update patient
# DELETE /api/patients/{id}/ - Delete patient

# Appointments:
# GET /api/appointments/ - List all appointments
# GET /api/appointments/upcoming/ - Get upcoming appointments
# POST /api/appointments/ - Create appointment
# GET /api/appointments/{id}/ - Get specific appointment
# PUT /api/appointments/{id}/ - Update appointment
# DELETE /api/appointments/{id}/ - Delete appointment
# POST /api/appointments/{id}/cancel/ - Cancel appointment

# Test Results:
# GET /api/test-results/ - List all test results
# GET /api/test-results/recent/ - Get recent test results
# POST /api/test-results/ - Create test result
# GET /api/test-results/{id}/ - Get specific test result
# PUT /api/test-results/{id}/ - Update test result
# DELETE /api/test-results/{id}/ - Delete test result

# Medications:
# GET /api/medications/ - List all medications
# GET /api/medications/active/ - Get active medications
# POST /api/medications/ - Create medication
# GET /api/medications/{id}/ - Get specific medication
# PUT /api/medications/{id}/ - Update medication
# DELETE /api/medications/{id}/ - Delete medication