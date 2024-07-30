# Use the official Python base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the files from the current directory to the working directory
COPY . .

# Install any necessary dependencies
RUN pip install -r requirements.txt

# Check if data.db is present in the data folder
RUN if [ ! -f data/data.db ]; then python initialize.py; fi

# Run the python script "main.py"
CMD ["python", "-u", "main.py"]