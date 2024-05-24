from datetime import datetime
from rest_framework import serializers

from features.utils.calculate_age import calculate_age
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
            'mzu_hc_id',
            'patient_type',
            'illness',
            'allergy',
            'age',
            'age_input',
            'employee',
            'student',
            'employee_dependent',
            'mzu_outsider',
        )

    def validate_age_input(self, value):
        """Validate the input age."""
        if value is not None:
            if value < 0 or value > 150:  # Basic validation for age
                raise serializers.ValidationError("Please enter a valid age.")
        return value

    # def create(self, validated_data):
    #     age = validated_data.pop('age_input', None)
    #     if age is not None:
    #         year_of_birth = datetime.now().year - age
    #         validated_data['year_of_birth'] = year_of_birth
    #     return super().create(validated_data)

    # def update(self, instance, validated_data):
    #     age = validated_data.pop('age_input', None)
    #     if age is not None:
    #         instance.year_of_birth = datetime.now().year - age
    #     return super().update(instance, validated_data)

    def get_age(self, obj):
        """Compute age from year_of_birth for output."""
        if obj.employee is not None:
            return calculate_age(obj.employee.date_of_birth)
        if obj.student is not None:
            return calculate_age(obj.student.date_of_birth) 
        if obj.employee_dependent is not None:
            return calculate_age(obj.employee_dependent.date_of_birth)
        if obj.mzu_outsider is not None:
            return obj.mzu_outsider.age
        return None

    def validate(self, data):
        """Validate the patient data."""
        patient_type = data.get('patient_type')
        employee = data.get('employee')
        student = data.get('student')
        employee_dependent = data.get('employee_dependent')
        mzu_outsider = data.get('mzu_outsider')

        related_fields = [employee, student, employee_dependent, mzu_outsider]
        if sum(bool(field) for field in related_fields) != 1:
            raise serializers.ValidationError("Exactly one related person (employee, student, employee dependent, or MZU outsider) must be set.")

        if patient_type == 'Employee Dependent' and not employee_dependent:
            raise serializers.ValidationError("Employee Dependent patients must have an associated employee dependent.")
        if patient_type == 'Student' and not student:
            raise serializers.ValidationError("Student patients must have an associated student.")
        if patient_type == 'Other' and not mzu_outsider:
            raise serializers.ValidationError("Other patients must have an associated MZU outsider patient.")
        if patient_type == 'Employee' and not employee:
            raise serializers.ValidationError("Employee patients must have an associated employee.")

        return data
