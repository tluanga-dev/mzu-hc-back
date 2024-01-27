

from datetime import datetime, timezone


def format_datetime_with_timezone_offset(datetime_str):
    """
    Format a datetime string with an explicit timezone offset and retain milliseconds.

    Args:
        datetime_str (str): The datetime string in the format 'YYYY-MM-DDTHH:MM:SS.mmmmmmZ'.

    Returns:
        str: The formatted datetime string with timezone offset in the format 'YYYY-MM-DDTHH:MM:SS.mmmmmm+HHMM'.
    """
    # Convert the string representation to a datetime object
    serializer_datetime = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S.%fZ')

    # Convert the datetime object to UTC timezone
    serializer_datetime_utc = serializer_datetime.replace(tzinfo=timezone.utc)

    # Format the datetime with an explicit timezone offset
    formatted_datetime = serializer_datetime_utc.strftime('%Y-%m-%dT%H:%M:%S.%f%z')

    return formatted_datetime

# Example usage:
serializer_data = {
    'id': 8,
    # Other fields...
    'date_time': '2024-01-27T16:32:47.250473Z'
}

serializer_data['date_time'] = format_datetime_with_timezone_offset(serializer_data['date_time'])
print(serializer_data['date_time'])  # Output: '2024-01-27T16:32:47.250473+0000'
