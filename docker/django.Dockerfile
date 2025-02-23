FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Run migrations and collect static files if needed
RUN python manage.py migrate
# (Optional) RUN python manage.py collectstatic --noinput

# Expose Django's default port
EXPOSE 8000

# Command to run the server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]