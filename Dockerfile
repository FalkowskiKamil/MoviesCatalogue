# Use the official Python base image with the desired version
FROM python:3.10.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /code

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install project dependencies
RUN pip install -r requirements.txt

# Copy the entire Flask project to the working directory
COPY . .

# Expose the port that your Flask app will listen on
EXPOSE 5000

# Specify the command to run when the container starts
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]