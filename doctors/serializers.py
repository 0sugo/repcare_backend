from rest_framework import serializers
from .models import Doctor
from patients.models import Appointment, Medication
from patients.serializers import PatientSerializer

class DoctorSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model= Doctor
        fields= '__all__'
        
    def get_full_name(self,obj):
        return f"Dr. {obj.user.get_full_name()}"

class DoctorAppointmentSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    
    class Meta:
        model= Appointment
        fileds= '__all__'
        
class DoctorMedicationSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    
    class Meta:
        model = Medication
        fields = '__all__'