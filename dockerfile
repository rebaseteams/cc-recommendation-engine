FROM alpine:latest

RUN apk update
RUN apk add py-pip
RUN apk add --no-cache python3-dev 
RUN pip install --upgrade pip
# need g++ to install pandas from requirement
RUN apk add g++

WORKDIR /app
COPY . /app
RUN pip --no-cache-dir install -r requirements.txt
EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]