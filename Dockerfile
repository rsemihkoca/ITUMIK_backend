# Builder stage
FROM python:3.10-alpine as compile-image

## virtualenv
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
FROM python:3.10-alpine as runtime-image

## copy Python dependencies from build image
COPY --from=compile-image /opt/py310 /opt/py310
COPY --from=compile-image /app /app

WORKDIR /app/main
## set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/opt/py310/bin:$PATH"

EXPOSE 8008

CMD ["/bin/sh"]
#CMD ["python3", "-m", "pytest", "*", "-v", "-o", "junit_family=xunit1", "--cov=../main", "--cov-report", "xml:../reports/coverage-cpu.xml", "--cov-report", "html:../reports/cov_html-cpu", "--junitxml=../reports/results-cpu.xml"]
# en son cmd çalışıyor