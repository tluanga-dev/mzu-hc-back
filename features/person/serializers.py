
import datetime
from rest_framework import serializers

from features.person.models import Employee, EmployeeDependent, MZUOutsider, Student


class EmployeeSerializerForDependent(serializers.ModelSerializer):
    organisation_unit=serializers.SerializerMethodField()

    def get_organisation_unit(self, obj):
        return {
            'id':  obj.organisation_unit.id,
            'name': obj.organisation_unit.name,
            'description': obj.organisation_unit.description, 
            'abbreviation' : obj.organisation_unit.abbreviation
        }
    class Meta:
        model = Employee
        fields = [
            'id',
            'name',
            'organisation_unit',
            'mzu_employee_id',
        ]

class EmployeeDependentSerializer(serializers.ModelSerializer):
    employee=EmployeeSerializerForDependent()
    age=serializers.SerializerMethodField()

    def get_age(self, obj):
       return obj.get_age()
    
    class Meta:
        model = EmployeeDependent
        fields = [
            'id',
            'mzu_employee_dependent_id',
            'name',
            'age',
            'gender',
            'relation',
            'date_of_birth',
            'employee',
            'is_active'
        ]


class EmployeeSerializer(serializers.ModelSerializer):
    date_of_birth = serializers.DateField(format='%d-%m-%Y')
    employee_dependents = EmployeeDependentSerializer(many=True, read_only=True)
    age=serializers.SerializerMethodField()
    organisation_unit=serializers.SerializerMethodField()

    def get_organisation_unit(self, obj):
        return {
            'id':  obj.organisation_unit.id,
            'name': obj.organisation_unit.name,
            'description': obj.organisation_unit.description, 
            'abbreviation' : obj.organisation_unit.abbreviation
        }


    def get_age(self, obj):
        today = datetime.date.today()
        return today.year - obj.date_of_birth.year - ((today.month, today.day) < (obj.date_of_birth.month, obj.date_of_birth.day))

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
            'age',
            'gender',
            'email',
            'mzu_employee_id',
            'organisation_unit',
            'employee_type',
            'designation',
            'mobile_no',
            'date_of_birth',
            'employee_dependents',
            'is_active'
        ]


class StudentSerializer(serializers.ModelSerializer):
    date_of_birth = serializers.DateField(format='%d-%m-%Y')
    age=serializers.SerializerMethodField()

    organisation_unit=serializers.SerializerMethodField()

    def get_organisation_unit(self, obj):
        return {
            'id':  obj.organisation_unit.id,
            'name': obj.organisation_unit.name,
            'description': obj.organisation_unit.description, 
            'abbreviation' : obj.organisation_unit.abbreviation
        }


    def get_age(self, obj):
        today = datetime.date.today()
        return today.year - obj.date_of_birth.year - ((today.month, today.day) < (obj.date_of_birth.month, obj.date_of_birth.day))

    
    class Meta:
        model = Student
        fields = [
            'id',
            'name',
            'age',
            'gender',
            'email',
            'mzu_student_id',
            'organisation_unit',
            # 'employee_type',
            # 'designation',
            'mobile_no',
            'date_of_birth',
             'programme',
            'is_active'
        ]

class MZUOutsiderSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = MZUOutsider
        fields = [
            'id',
            'name',
            'age',
        ]