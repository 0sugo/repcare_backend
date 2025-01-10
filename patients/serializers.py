from rest_framework import serializers
from .models import Patient, TestResult, Medication, Appointment

class PatientSerializer(serializers.ModelSerializer):
    user_full_name = serializers.CharField(source='user.get_full_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')
    
    def create(self,validated_data):
        user = self.context['request'].user
        patient = Patient.objects.create(user=user, **validated_data)
        return patient

class TestResultSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.user.get_full_name', read_only=True)
    
    class Meta:
        model = TestResult
        fields = '__all__'
        read_only_fields = ('created_at', 'reviewed_at')

class MedicationSerializer(serializers.ModelSerializer):
    prescribed_by_name = serializers.CharField(source='prescribed_by.user.get_full_name', read_only=True)
    days_remaining = serializers.SerializerMethodField()
    
    class Meta:
        model = Medication
        fields = '__all__'

    def get_days_remaining(self, obj):
        from django.utils import timezone
        today = timezone.now().date()
        return (obj.end_date - today).days if obj.end_date >= today else 0

class AppointmentSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.user.get_full_name', read_only=True)
    doctor_specialty = serializers.CharField(source='doctor.specialty', read_only=True)
    is_video_available = serializers.SerializerMethodField()
    
    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ('created_at',)

    def get_is_video_available(self, obj):
        return bool(obj.video_link and obj.appointment_type == 'video')