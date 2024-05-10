from rest_framework import serializers

from features.person.models import Employee



class EmployeeSerializer(serializers.ModelSerializer):
    date_of_birth = serializers.DateField(format='%d-%m-%Y')


    class Meta:
        model = Employee
        fields = [
            'id',
            'name',
            'gender',
            'email',
            'employee_id',
            'department',
            'designation',
            'mobile_no',
            'date_of_birth',
            'is_active'
        ]