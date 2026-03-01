FROM python:3.9-alpine3.13

ENV PYTHONUNBUFFERED 1

WORKDIR /app

ARG DEV=false
COPY requirements.txt requirements.dev.txt .
RUN python -m venv /py && \
  /py/bin/pip install --upgrade pip && \
  /py/bin/pip install -r requirements.txt && \
  if [ "$DEV" = "true" ]; then /py/bin/pip install -r requirements.dev.txt; fi && \
  rm -f requirements.txt requirements.dev.txt && \
  adduser \
    --disabled-password \
    --no-create-home \
    django-user

ENV PATH="/py/bin:$PATH"

COPY ./app /app

EXPOSE 8000

USER django-user

# Example for development
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Or for production (if you add gunicorn to requirements.txt)
# CMD ["gunicorn", "your_project.wsgi:application", "--bind", "0.0.0.0:8000"]