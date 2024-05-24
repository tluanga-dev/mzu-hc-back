from rest_framework import serializers
from django.db import transaction
from features.inventory_transaction.inventory_transaction.models import ItemStockInfo
from features.item.models import Item
from features.medicine.serializers import MedicineDosageSerializer
from features.patient.models import Patient
from features.person.models import MZUOutsider, Student, Employee, EmployeeDependent
from features.prescription.models import Prescription, PrescriptionItem
from features.medicine.models import MedicineDosage, MedicineDosageTiming
from features.patient.serializers import PatientSerializer
from features.person.serializers import MZUOutsiderSerializer
from features.prescription.serializers.prescription_serializer import PrescriptionSerializer


class CreatePrescriptionSerializer(serializers.Serializer):
    patient_type = serializers.ChoiceField(choices=Patient.PATIENT_TYPE_CHOICES)
    patient_data = PatientSerializer()
    prescription_data = serializers.JSONField()  # We'll manually handle nested validation
    mzu_outsider_data = MZUOutsiderSerializer(required=False)

    def validate(self, attrs):
        patient_type = attrs.get('patient_type')
        mzu_outsider_data = attrs.get('mzu_outsider_data')

        if patient_type == 'Other' and not mzu_outsider_data:
            raise serializers.ValidationError("MZUOutsider data is required for 'Other' patient type.")
        
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        patient_type = validated_data.get('patient_type')
        patient_data = validated_data.get('patient_data')
        prescription_data = validated_data.get('prescription_data')
        mzu_outsider_data = validated_data.get('mzu_outsider_data', None)

        try:
            # Create or get patient based on patient_type
            if patient_type == 'Employee':
                employee = Employee.objects.get(pk=patient_data.pop('employee'))
                patient, created = Patient.objects.get_or_create(employee=employee, defaults=patient_data)
            elif patient_type == 'Student':
                student = Student.objects.get(pk=patient_data.pop('student'))
                patient, created = Patient.objects.get_or_create(student=student, defaults=patient_data)
            elif patient_type == 'Employee Dependent':
                employee_dependent = EmployeeDependent.objects.get(pk=patient_data.pop('employee_dependent'))
                patient, created = Patient.objects.get_or_create(employee_dependent=employee_dependent, defaults=patient_data)
            elif patient_type == 'Other':
                mzu_outsider_patient = MZUOutsider.objects.create(**mzu_outsider_data)
                patient, created = Patient.objects.get_or_create(mzu_outsider_patient=mzu_outsider_patient, defaults=patient_data)
            else:
                raise serializers.ValidationError("Invalid patient type or missing MZUOutsider data")

            # Create prescription with the associated patient
            prescription_data['patient'] = patient.id

            prescribed_item_set_data = prescription_data.pop('prescribed_item_set', [])
            prescription = Prescription.objects.create(**prescription_data)

            for prescribed_item_data in prescribed_item_set_data:
                medicine_dosage_list_data = prescribed_item_data.pop('dosages', [])
                prescription_item = PrescriptionItem.objects.create(**prescribed_item_data, prescription=prescription)
                medicine = prescription_item.medicine

                for medicine_dosage_data in medicine_dosage_list_data:
                    medicine_dosage_timing_set_data = medicine_dosage_data.pop('medicine_dosage_timing_set', [])
                    medicine_dosage = MedicineDosage.objects.create(**medicine_dosage_data, medicine=medicine)
                    prescription_item.dosages.add(medicine_dosage)

                    for medicine_dosage_timing_data in medicine_dosage_timing_set_data:
                        MedicineDosageTiming.objects.create(**medicine_dosage_timing_data, medicine_dosage=medicine_dosage)

            return {
                'patient': PatientSerializer(patient).data,
                'prescription': PrescriptionSerializer(prescription).data
            }

        except Exception as e:
            raise serializers.ValidationError(f"Error occurred: {str(e)}")
        






class PrescribeMedicineItemSerializer(serializers.ModelSerializer):
    quantity_in_stock=serializers.SerializerMethodField()
    def get_quantity_in_stock(self, obj):
        # quantity_in_stock=ItemStockInfo.get_latest_by_item_id(obj.id).quantity_in_stock
        #  Fetch the latest stock information by item ID
        item_stock_info = ItemStockInfo.get_latest_by_item_id(obj.id)

        # Check if item_stock_info is None and assign 0 if so, otherwise get the quantity_in_stock
        quantity_in_stock = 0 if item_stock_info is None else item_stock_info.item_quantity_in_stock
        return quantity_in_stock

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Accessing only the name of the unit of measurement
        representation['unit_of_measurement'] = instance.unit_of_measurement.abbreviation if instance.unit_of_measurement else None
        return representation

    class Meta:
        model = Item
        fields = ['id', 'name', 'contents', 'unit_of_measurement','quantity_in_stock']






class PrescriptionItemSerializer(serializers.ModelSerializer):
    dosages = MedicineDosageSerializer(many=True)
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['medicine'] = PrescribeMedicineItemSerializer(instance.medicine).data
        return representation

    class Meta:
        model = PrescriptionItem
        fields = ['id', 'note', 'dosages', 'medicine']

    def create(self, validated_data):
        dosages_data = validated_data.pop('dosages', [])
        item_data = validated_data.pop('item')
        item = Item.objects.get(id=item_data['id'])  # Assuming existence or use ItemSerializer to create
        prescription_item = PrescriptionItem.objects.create(item=item, **validated_data)
        for dosage_data in dosages_data:
            dosage = MedicineDosageSerializer().create(dosage_data)
            prescription_item.dosages.add(dosage)
        return prescription_item
    


class PrescriptionSerializer(serializers.ModelSerializer):
    prescribed_item_set = PrescriptionItemSerializer(many=True)
    date_and_time = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")

    class Meta:
        model = Prescription
        fields = [
            'id',
            'code', 
            'patient', 
            'chief_complaints',
            'diagnosis',
            'advice_and_instructions', 
            'date_and_time', 
            'prescription_dispense_status', 
            'prescribed_item_set'
        ]
        read_only_fields = ['code']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['patient'] = PatientSerializer(instance.patient).data
        # representation['doctor'] = PrescriptionPersonSerializer(instance.doctor).data
        return representation
    


class UpdatePrescriptionSerializer(serializers.Serializer):
    patient_type = serializers.ChoiceField(choices=Patient.PATIENT_TYPE_CHOICES)
    patient_data = PatientSerializer()
    prescription_data = serializers.JSONField()  # We'll manually handle nested validation
    mzu_outsider_data = MZUOutsiderSerializer(required=False)

    def validate(self, attrs):
        patient_type = attrs.get('patient_type')
        mzu_outsider_data = attrs.get('mzu_outsider_data')

        if patient_type == 'Other' and not mzu_outsider_data:
            raise serializers.ValidationError("MZUOutsider data is required for 'Other' patient type.")
        
        return attrs

    @transaction.atomic
    def update(self, instance, validated_data):
        patient_type = validated_data.get('patient_type')
        patient_data = validated_data.get('patient_data')
        prescription_data = validated_data.get('prescription_data')
        mzu_outsider_data = validated_data.get('mzu_outsider_data', None)

        try:
            # Update or get patient based on patient_type
            if patient_type == 'Employee':
                employee = Employee.objects.get(pk=patient_data.pop('employee'))
                patient, created = Patient.objects.update_or_create(employee=employee, defaults=patient_data)
            elif patient_type == 'Student':
                student = Student.objects.get(pk=patient_data.pop('student'))
                patient, created = Patient.objects.update_or_create(student=student, defaults=patient_data)
            elif patient_type == 'Employee Dependent':
                employee_dependent = EmployeeDependent.objects.get(pk=patient_data.pop('employee_dependent'))
                patient, created = Patient.objects.update_or_create(employee_dependent=employee_dependent, defaults=patient_data)
            elif patient_type == 'Other':
                mzu_outsider_patient = MZUOutsider.objects.create(**mzu_outsider_data)
                patient, created = Patient.objects.update_or_create(mzu_outsider_patient=mzu_outsider_patient, defaults=patient_data)
            else:
                raise serializers.ValidationError("Invalid patient type or missing MZUOutsider data")

            # Update prescription with the associated patient
            prescription_data['patient'] = patient.id

            # Handle prescribed items and nested dosages
            prescribed_item_set_data = prescription_data.pop('prescribed_item_set', [])
            
            # Update the prescription instance
            for attr, value in prescription_data.items():
                setattr(instance, attr, value)
            instance.save()

            # Clear existing prescribed items
            instance.prescribed_item_set.all().delete()

            # Re-create prescribed items
            for prescribed_item_data in prescribed_item_set_data:
                medicine_dosage_list_data = prescribed_item_data.pop('dosages', [])
                prescription_item = PrescriptionItem.objects.create(**prescribed_item_data, prescription=instance)
                medicine = prescription_item.medicine

                for medicine_dosage_data in medicine_dosage_list_data:
                    medicine_dosage_timing_set_data = medicine_dosage_data.pop('medicine_dosage_timing_set', [])
                    medicine_dosage = MedicineDosage.objects.create(**medicine_dosage_data, medicine=medicine)
                    prescription_item.dosages.add(medicine_dosage)

                    for medicine_dosage_timing_data in medicine_dosage_timing_set_data:
                        MedicineDosageTiming.objects.create(**medicine_dosage_timing_data, medicine_dosage=medicine_dosage)

            return {
                'patient': PatientSerializer(patient).data,
                'prescription': PrescriptionSerializer(instance).data
            }

        except Exception as e:
            raise serializers.ValidationError(f"Error occurred: {str(e)}")
