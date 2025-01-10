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
        today = timezone.now().date()
        
        metrics = {
            'consultations': {
                'total': Appointment.objects.filter(patient=patient).count(),
                'upcoming': Appointment.objects.filter(
                    patient=patient,
                    date__gte=today,
                    status__in=['scheduled', 'confirmed']
                ).count(),
                'last_visit': Appointment.objects.filter(
                    patient=patient,
                    status='completed'
                ).order_by('-date').values_list('date', flat=True).first()
            },
            'medications': {
                'active': Medication.objects.filter(
                    patient=patient,
                    end_date__gte=today,
                    is_active=True
                ).count(),
                'adherence': Medication.objects.filter(
                    patient=patient,
                    is_active=True
                ).aggregate(avg_adherence=models.Avg('adherence_rate'))['avg_adherence'] or 0
            },
            'test_results': {
                'pending': TestResult.objects.filter(
                    patient=patient,
                    status='pending'
                ).count(),
                'available': TestResult.objects.filter(
                    patient=patient,
                    status='available'
                ).count()
            }
        }
        return Response(metrics)

class AppointmentViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        return Appointment.objects.filter(patient__user=self.request.user)

    @action(detail=False, methods=['GET'])
    def upcoming(self, request):
        upcoming = self.get_queryset().filter(
            date__gte=timezone.now().date(),
            status__in=['scheduled', 'confirmed']
        ).select_related('doctor').order_by('date', 'time')
        return Response(self.get_serializer(upcoming, many=True).data)

    @action(detail=True, methods=['POST'])
    def cancel(self, request, pk=None):
        appointment = self.get_object()
        appointment.status = 'cancelled'
        appointment.save()
        return Response({'status': 'appointment cancelled'})

class TestResultViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TestResultSerializer

    def get_queryset(self):
        return TestResult.objects.filter(patient__user=self.request.user)

    @action(detail=False, methods=['GET'])
    def recent(self, request):
        recent = self.get_queryset().order_by('-date')[:5]
        return Response(self.get_serializer(recent, many=True).data)

class MedicationViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MedicationSerializer

    def get_queryset(self):
        return Medication.objects.filter(patient__user=self.request.user)

    @action(detail=False, methods=['GET'])
    def active(self, request):
        today = timezone.now().date()
        active = self.get_queryset().filter(
            end_date__gte=today,
            is_active=True
        ).order_by('name')
        return Response(self.get_serializer(active, many=True).data)