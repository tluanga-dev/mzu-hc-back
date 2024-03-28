#!/bin/bash

# Navigate to your project directory
cd /home/ubuntu/mzu-hc-back

# Pull the latest code from GitHub
if ! git pull origin main; then
    echo "Failed to pull from GitHub. Exiting."
    exit 1
fi


# Assuming you're using a Python virtual environment, activate it
source /home/ubuntu/mzu-hc-back/venv/bin/activate

# Install any new dependencies
pip install -r requirements.txt

# Make migrations (Generate new migration files)
python manage.py makemigrations

# Apply migrations (Apply the generated migration files to the database)
python manage.py migrate

# Collect static files (Django projects)
python manage.py collectstatic --noinput

# Restart Gunicorn (adjust the service name as necessary)
sudo systemctl restart gunicorn

# Restart Nginx
sudo systemctl restart nginx

echo "Deployment completed."
