from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Doctor
from patients.models import Appointment, TestResult, Medication
from .serializers import (
    DoctorSerializer, DoctorAppointmentSerializer,
    DoctorTestResultSerializer, DoctorMedicationSerializer
)

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if not self.request.user.is_staff:
            return Doctor.objects.filter(user=self.request.user)
        return Doctor.objects.all()

    @action(detail=True, methods=['patch'])
    def update_availability(self, request, pk=None):
        doctor = self.get_object()
        status = request.data.get('availability_status')
        if status in dict(Doctor.AVAILABILITY_CHOICES).keys():
            doctor.availability_status = status
            doctor.save()
            return Response({'status': 'Availability updated successfully'})
        return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True)
    def dashboard_stats(self, request, pk=None):
        doctor = self.get_object()
        today = timezone.now().date()
        
        # Get today's appointments
        todays_appointments = Appointment.objects.filter(
            doctor=doctor,
            date=today
        )
        
        # Get pending test results
        pending_results = TestResult.objects.filter(
            doctor=doctor,
            status='pending'
        )
        
        # Get active medications
        active_medications = Medication.objects.filter(
            prescribed_by=doctor,
            is_active=True
        )

        return Response({
            'total_appointments_today': todays_appointments.count(),
            'pending_appointments': todays_appointments.filter(status='scheduled').count(),
            'completed_appointments': todays_appointments.filter(status='completed').count(),
            'pending_test_results': pending_results.count(),
            'active_prescriptions': active_medications.count()
        })

    @action(detail=True)
    def upcoming_appointments(self, request, pk=None):
        doctor = self.get_object()
        today = timezone.now().date()
        appointments = Appointment.objects.filter(
            doctor=doctor,
            date__gte=today,
            status__in=['scheduled', 'confirmed']
        ).order_by('date', 'time')
        serializer = DoctorAppointmentSerializer(appointments, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def critical_test_results(self, request, pk=None):
        doctor = self.get_object()
        results = TestResult.objects.filter(
            doctor=doctor,
            priority='high',
            status__in=['pending', 'available']
        ).order_by('-created_at')
        serializer = DoctorTestResultSerializer(results, many=True)
        return Response(serializer.data)