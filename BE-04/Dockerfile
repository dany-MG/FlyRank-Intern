#Using a lightweight Python image as the base image
FROM python:3.10-slim

#Setting the working directory inside the container
WORKDIR /app

#Copying the requirements file to the working directory
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#Copying the rest of the application code to the working directory
COPY . .

#Exposing the port the app runs on
EXPOSE 3000

#Starting the application using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]

