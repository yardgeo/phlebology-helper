FROM tiangolo/uwsgi-nginx-flask:python3.6

RUN mkdir -p /usr/src/phlebology-helper-backend
WORKDIR /usr/src/phlebology-helper-backend

COPY requirements.txt /usr/src/phlebology-helper-backend/

#COPY nginx.conf /etc/nginx/conf.d/custom.conf

RUN python3 -m pip install -r requirements.txt --no-cache-dir

COPY . /usr/src/phlebology-helper-backend
COPY nginx-ssl.conf /etc/nginx/conf.d/nginx-ssl.conf

COPY prestart.sh /app/prestart.sh
