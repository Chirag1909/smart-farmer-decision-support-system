# Use stable Python version (IMPORTANT: NOT 3.13/3.14)
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port
EXPOSE 10000

# Run app
CMD ["gunicorn", "-b", "0.0.0.0:10000", "app:app"]