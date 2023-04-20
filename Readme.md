### Install python virtual env and create a new virtual env
```
pip install virtualenv

virtualenv --version

virtualenv b-py-client
```

### To run server 
```
uvicorn main:app
```

### Run in docker
```
docker build -t bc-py-client .
docker run -p 8080:80  bc-py-client:latest
```