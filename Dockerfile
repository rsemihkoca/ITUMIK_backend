# syntax=docker/dockerfile:1

# Builder stage
FROM python:3.10-alpine as compile-image

## set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV VIRTUAL_ENV=/opt/py310
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy requirements.txt
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt && rm -rf /var/cache/apk/*

# Copy the rest of the application files
COPY . /app

# Test stage
FROM compile-image as  test-image

WORKDIR /app/main

EXPOSE 8008

CMD ["/bin/sh"]

# Runtime stage
FROM compile-image as runtime-image

# Copy Python dependencies and the application from the compile-image stage
#COPY --from=compile-image /opt/py310 /opt/py310
#COPY --from=compile-image /app /app

WORKDIR /app

EXPOSE 8008

# Run the main/debug.py if tests pass
CMD ["python3", "main/debug.py"]