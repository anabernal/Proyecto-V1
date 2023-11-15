FROM python:3.8-alpine
#
ENV DEBUG=True
ENV SECRET_KEY="django-insecure-3^15q=16uthglk3f18!su3w_eoefl1$(!11yni5gzwbu@lrznq"
ENV DATABASE="finanzas-demo"
ENV USER_DB="postgres"
ENV PASS_DB=1902
ENV HOST_DB="localhost"
ENV PORT_DB="5432"
#
COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install pipenv
RUN apk add --update --no-cache --virtual .tmp gcc libc-dev libpq-dev python3-dev
RUN pip install -r requirements.txt
WORKDIR /app
COPY . .
EXPOSE 8088
#CMD ["python", "manage.py", "runserver", "127.0.0.1:8000"]
ENTRYPOINT python manage.py runserver 0.0.0.0:8088





#WORKDIR /Finanzas
#COPY requirements.txt /Finanzas/
#RUN /bin/sh -c pip install --no-cache-dir -r requirements.txt
#COPY . /Finanzas/
#RUN /bin/sh -c apk add --update --no-cache --virtual .tmp gcc libc-dev
#RUN /bin/sh -c pip install --no-cache-dir -r requirements.txt

#ENTRYPOINT python manage.py runserver 0.0.0.0:8082