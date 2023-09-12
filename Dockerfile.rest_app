# Official Python runtime as the base image
FROM python:3.11.0

# Working directory in the container
WORKDIR /app

# Declare the build argument as an environmental variable
ARG DB_USER

ARG DB_PASS

ENV FLASK_APP=rest_app.py

ENV FLASK_RUN_HOST=127.0.0.1

ENV DB_USERNAME=$DB_USER

ENV DB_PASSWORD=$DB_PASS

# Copy the requirements file into the container
COPY requirements.txt requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files into the container
COPY . .

# Expose the port that the app runs on
EXPOSE 5000

# Define the command to run your Flask app
CMD python rest_app.py $DB_USERNAME $DB_PASSWORD