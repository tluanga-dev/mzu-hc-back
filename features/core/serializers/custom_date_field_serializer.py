from rest_framework import serializers

from features.core.utils.convert_date import DateConverter




class CustomDateField(serializers.DateField):
    def to_representation(self, value):
        try:
            value = value.strftime("%d-%m-%Y")
            return value
        except ValueError as e:
            print('There is an error- ', e)

    def to_internal_value(self, data):
        return DateConverter.convert_date_format(data)