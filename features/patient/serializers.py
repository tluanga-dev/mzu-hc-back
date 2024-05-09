from datetime import datetime
from rest_framework import serializers
from .models import Patient
from datetime import datetime
from rest_framework import serializers
from .models import Patient

class PatientSerializer(serializers.ModelSerializer):
    # Output field, computed from year_of_birth
    age = serializers.SerializerMethodField()
    # Input field, not saved directly
    age_input = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Patient
        fields = (
            'id', 
            'name',
            'patient_type',
            'gender', 
            'age',
            'year_of_birth',  # for output
            'age_input',  # for input
            'student_id',
            'mobile_number'
        )

    def validate_age_input(self, value):
        """Validate the input age."""
        if value < 0 or value > 150:  # Basic validation for age
            raise serializers.ValidationError("Please enter a valid age.")
        return value

    def create(self, validated_data):
        age = validated_data.pop('age_input', None)
        if age is not None:

            year_of_birth = datetime.now().year - age
            
            validated_data['year_of_birth'] = year_of_birth
        return super().create(validated_data)

    def update(self, instance, validated_data):
        age = validated_data.pop('age_input', None)
        if age is not None:
            instance.year_of_birth = datetime.now().year - age
        return super().update(instance, validated_data)

    def get_age(self, obj):
        """Compute age from year_of_birth for output."""
        return datetime.now().year - obj.year_of_birth
