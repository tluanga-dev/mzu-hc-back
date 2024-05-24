from rest_framework import serializers
from datetime import datetime

from features.utils.convert_date import DateConverter

class BaseSerializer(serializers):
    date_and_time = serializers.DateTimeField(format="%d-%m-%Y %H:%M")
    created_at = serializers.DateTimeField(format="%d-%m-%Y %H:%M")
    updated_at = serializers.DateTimeField(format="%d-%m-%Y %H:%M")

    def to_internal_value(self, data):
        # Convert the incoming date_and_time to the database format
        if 'date_and_time' in data:
            try:
                data['date_and_time'] = DateConverter.convert_date_time_format_to_django_default(
                    data['date_and_time']
                ) 
            except ValueError:
                raise serializers.ValidationError({"date_and_time": "Date and time must be in 'dd-mm-yyyy hh:mm' format"})
        
        if 'created_at' in data:
            try:
                data['created_at'] = DateConverter.convert_date_time_format_to_django_default(
                    data['created_at']
                ) 
            except ValueError:
                raise serializers.ValidationError({"created_at": "Date and time must be in 'dd-mm-yyyy hh:mm' format"})
            
        if 'updated_at' in data:
            try:
                data['updated_at'] = DateConverter.convert_date_time_format_to_django_default(
                    data['updated_at']
                ) 
            except ValueError:
                raise serializers.ValidationError({"updated_at": "Date and time must be in 'dd-mm-yyyy hh:mm' format"})

        
        return super().to_internal_value(data)