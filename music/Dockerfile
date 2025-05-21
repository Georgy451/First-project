FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install Pillow
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]