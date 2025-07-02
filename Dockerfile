# Dockerfile

# --- Stage 1: Build Stage ---
# Use a slim, modern Python image to install dependencies.
FROM python:3.12.10-slim-bullseye AS builder

# Set environment variables to prevent .pyc file generation and ensure output is sent straight to the console.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Copy the requirements file first to leverage Docker's layer caching.
COPY requirements.txt .

# Install Python dependencies.
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt


# --- Stage 2: Final Production Stage ---
# Use the same slim Python image for the final build.
FROM python:3.12.10-slim-bullseye

# Create a dedicated, non-root user and group for the application for enhanced security.
RUN addgroup --system app && adduser --system --group app

# Set up the application home directory.
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME

# Copy the installed Python packages from the builder stage.
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

# Copy the application source code and the .env file.
COPY ./src $APP_HOME/src
COPY .env $APP_HOME/.env

# Grant ownership of all application files to the non-root user.
RUN chown -R app:app $APP_HOME

# Switch to the non-root user.
USER app

# Expose the internal port the app will run on. Nginx will connect to this.
EXPOSE 8000

# The command to run the application using a production-grade ASGI server (Uvicorn).
# The host is set to 0.0.0.0 to accept connections from Nginx.
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
