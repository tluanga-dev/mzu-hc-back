from datetime import datetime


class DateConverter:
    @staticmethod
    def convert_date_time_format_to_django_default(date_str):
        try:
            # Strip leading and trailing whitespace
            date_str = date_str.strip()

            # Check if time is included in the date_str
            if ':' in date_str:
                # Parse the date string into a datetime object with time
                dt = datetime.strptime(date_str, '%d-%m-%Y %H:%M')
                # Format the datetime object into the new format with time
                date_time = dt.strftime('%Y-%m-%d %H:%M:%S')
            else:
                # Parse the date string into a datetime object without time
                dt = datetime.strptime(date_str, '%d-%m-%Y')
                # Format the datetime object into the new format without time
                date_time = dt.strftime('%Y-%m-%d')
        except ValueError as e:
            # Handle the error gracefully
            print(f"Error occurred while converting date: {e}")
            date_time = None

        return date_time


    @staticmethod
    def convert_date_format(date_str):
        # Strip leading and trailing whitespace
        date_str = date_str.strip()

        # Parse the date string into a datetime object
        dt = datetime.strptime(date_str, '%d-%m-%Y')

        # Format the datetime object into the new format and set time to 00:00:00
        return dt.strftime('%Y-%m-%d')

    @staticmethod
    def format_date_string(date_str):
        """
        Convert a date string from the format YYYY-MM-DDTHH:MM:SSZ to DD/MM/YYYY.

        Parameters:
        date_str (str): The date string to convert.

        Returns:
        str: The date string in the format DD/MM/YYYY.
        """
        dt = datetime.strptime(date_str.split('T')[0], '%Y-%m-%d')
        return dt.strftime('%d-%m-%Y')

    @staticmethod
    def datetime_to_string(dt):
        """
        Convert a datetime object to a string in the format DD/MM/YYYY.

        Parameters:
        dt (datetime): The datetime object to convert.

        Returns:
        str: The datetime object as a string in the format DD/MM/YYYY.
        """
        return dt.strftime('%d-%m-%Y')

    @staticmethod
    def convert_date_format(date_str):
        try:
            print('-----inside convert date format------')
            print(date_str)
            # Strip leading and trailing whitespace
            date_str = date_str.strip()

            # Parse the date string into a datetime object
            dt = datetime.strptime(date_str, '%d-%m-%Y')

            # Format the datetime object into the new format and set time to 00:00:00
            # new_date = dt.strftime('%Y-%m-%d')
            # print('new date',new_date)
            print('return new date')
            return dt
        except ValueError as e:
            print('error',e)

    
    @staticmethod
    def format_date_string(date_str):
        """
        Convert a date string from the format YYYY-MM-DDTHH:MM:SSZ to DD/MM/YYYY.

        Parameters:
        date_str (str): The date string to convert.

        Returns:
        str: The date string in the format DD/MM/YYYY.
        """
        dt = datetime.strptime(date_str.split('T')[0], '%Y-%m-%d')
        return dt.strftime('%d-%m-%Y')


 
    @staticmethod
    def datetime_to_string(dt):
        """
        Convert a datetime object to a string in the format DD/MM/YYYY.

        Parameters:
        dt (datetime): The datetime object to convert.

        Returns:
        str: The datetime object as a string in the format DD/MM/YYYY.
        """
        return dt.strftime('%d-%m-%Y')

    # Usage:
    # dt = datetime(2023, 12, 28, 23, 59, 59)
    # print(datetime_to_string(dt))  # Outputs: 28/12/2023