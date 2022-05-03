FROM nickgryg/alpine-pandas:latest

RUN apk update
RUN apk add py-pip
RUN apk add --no-cache python3 py3-pip
RUN pip install --upgrade pip
# need g++ to install pandas from requirement

RUN pip install psycopg2-binary
RUN pip install flask
RUN pip install SQLAlchemy
RUN pip install pandas
RUN apk add g++

WORKDIR /app
COPY . /app
RUN pip --no-cache-dir install -r requirements.txt
EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]