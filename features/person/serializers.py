from rest_framework import serializers

from features.person.models import Employee, EmployeeDependent


class EmployeeDependentSerializer(serializers.ModelSerializer):
    # date_of_birth = serializers.DateField(format='%d-%m-%Y')

    class Meta:
        model = EmployeeDependent
        fields = [
            'id',
            'name',
            'relation',
            'date_of_birth',
            'employee',
            'is_active'
        ]


class EmployeeSerializer(serializers.ModelSerializer):
    date_of_birth = serializers.DateField(format='%d-%m-%Y')
    employee_dependents = EmployeeDependentSerializer(many=True, read_only=True)

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation['employee_dependents'] = EmployeeDependentSerializer(
    #         instance.employee_dependents.all(), many=True
    #     ).data
    #     return representation
    class Meta:
        model = Employee
        fields = [
            'id',
            'name',
            'gender',
            'email',
            'mzu_employee_id',
            'department',
            'designation',
            'mobile_no',
            'date_of_birth',
            'employee_dependents',
            'is_active'
        ]


