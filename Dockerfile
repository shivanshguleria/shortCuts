# 
FROM python:3.12.0-slim

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./  /code/
RUN cd code
# 

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]

#flyctl launch --dockerfile ./Dockerfile