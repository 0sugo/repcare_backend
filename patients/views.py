from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from django.utils import timezone
from patients.models import Patient, Appointment, TestResult, Medication
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .serializers import PatientSerializer, AppointmentSerializer, TestResultSerializer, MedicationSerializer
from django.db import models


class PatientViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PatientSerializer

    def get_queryset(self):
        return Patient.objects.filter(user=self.request.user)

    @action(detail=False, methods=['GET'])
    def dashboard_metrics(self, request):
        patient = self.get_queryset().first()
        
        # Calculate metrics
        appointments = Appointment.objects.filter(patient=patient)
        medications = Medication.objects.filter(patient=patient)
        test_results = TestResult.objects.filter(patient=patient)
        
        metrics = {
            'consultations': {
                'total': appointments.count(),
                'upcoming': appointments.filter(
                    date__gte=timezone.now().date(),
                    status='confirmed'
                ).count(),
                'last_visit': appointments.filter(
                    status='completed'
                ).order_by('-date').first().date if appointments.exists() else None
            },
            'medications': {
                'active': medications.filter(
                    end_date__gte=timezone.now().date()
                ).count(),
                'adherence': medications.aggregate(
                    avg_adherence=models.Avg('adherence_rate')
                )['avg_adherence']
            },
            'test_results': {
                'pending': test_results.filter(status='pending').count(),
                'available': test_results.filter(status='available').count()
            }
        }
        return Response(metrics)

class AppointmentViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        return Appointment.objects.filter(patient__user=self.request.user)

    @action(detail=False, methods=['GET'])
    def upcoming(self):
        upcoming = self.get_queryset().filter(
            date__gte=timezone.now().date(),
            status='confirmed'
        ).order_by('date', 'time')
        serializer = self.get_serializer(upcoming, many=True)
        return Response(serializer.data)

class TestResultViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TestResultSerializer

    def get_queryset(self):
        return TestResult.objects.filter(patient__user=self.request.user)

class MedicationViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MedicationSerializer

    def get_queryset(self):
        return Medication.objects.filter(patient__user=self.request.user)

    
