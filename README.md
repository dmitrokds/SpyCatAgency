# SpyCatAgency

## From task

https://develops.notion.site/Python-engineer-test-assessment-the-Spy-Cat-Agency-2760fe54b07b80fb9c04f4016b2ad26b

## Description

This task involves building a CRUD application. The goal is to create a system that showcases my understanding in building RESTful APIs, interacting with SQL-like databases, and integrating third-party services.

## Run

### 1

Copy my repository
```
git clone https://github.com/dmitrokds/SpyCatAgency.git
```

### 2

Create config.py inside project folder

My ```config.py``` that I have used
```
DB_URL = "agency.db"

BreadsUrl = "https://api.thecatapi.com/v1/breeds"

breeds = []

API_KEY = "test"
```

### 3

Create docker container and run it

BUILD
```
docker build -t spy_cat_agency .
```

RUN
```
docker run -d --name spy_cat_agency -p 8000:8000 spy_cat_agency
```

SHOW LOGS
```
docker logs spy_cat_agency -f
```
