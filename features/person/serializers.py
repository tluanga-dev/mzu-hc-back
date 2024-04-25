from rest_framework import serializers

from features.person.models import Department, Patient, Person, PersonType

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


class PersonTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonType
        fields = "__all__"

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model=Patient
        fields='__all__'

# class PersonSerializer(serializers.ModelSerializer):
#     person_type=serializers.SerializerMethodField()
#     department=serializers.SerializerMethodField()

#     def to_representation(self, instance):
        

#         return 

#     def get_person_type(self, person_type):
#         try:
#             person_type_obj = PersonType.objects.get(id=person_type)
#             return {
#                 'id': person_type_obj.id,
#                 'name': person_type_obj.name
#             }
#         except PersonType.DoesNotExist:
#             return None
        
#     def get_department(self, department):
#         try:
#             department_obj = Department.objects.get(id=department)
#             return {
#                 'id': department_obj.id,
#                 'name': department_obj.name
#             }

class PersonTypeSerializerForPerson(serializers.ModelSerializer):
    class Meta:
        model = PersonType
        fields = ['id', 'name','description','abbreviation']


class PersonSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        
    #     self.fields['department'] = DepartmentSerializer(read_only=True)

        self.fields['person_type'] = PersonTypeSerializerForPerson(read_only=True)
        return super().to_representation(instance)

    class Meta:
        model = Person
        fields = [
            'id',
            'name',
            'email',
            'mzu_id',
            'department',
            'designation',
            'person_type',
            'mobile_no',
            'is_active'
        ]