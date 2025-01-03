

FROM python:3.10

# Establece variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app


COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt


COPY . /app/

RUN useradd -m myuser
USER myuser


EXPOSE 8000

# Comando por defecto para ejecutar la aplicación
CMD ["sh", "-c", "python manage.py migrate && python manage.py load_initial_data && python manage.py runserver 0.0.0.0:8000"]
