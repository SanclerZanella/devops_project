FROM python:3.7-alpine
WORKDIR /app
COPY rest_app.py /app
RUN pip install flask
EXPOSE 5000
VOLUME /app/logs
CMD python3 main.py