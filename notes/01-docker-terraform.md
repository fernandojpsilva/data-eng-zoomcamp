## Docker basics concepts

To run a docker image in interactive mode (-it) and be able to interact via terminal, we use the following command where 'bash' is a parameter to our image 'ubuntu':

`docker run -it ubuntu bash`

This docker container will be stateless.: any changes done inside a container will NOT be saved when the container is killed and started again. This is an advantage because it allows us to restore any container to its initial state in a reproducible manner, but we will have to store data elsewhere if we need to do so; a common way to do so is with volumes.

To build a docker image from a 'Dockerfile', we use the command:

`docker build -t test:pandas .` 

and run it with:

`docker run -it test:pandas 2021-01-15`

where '2021-01-15' is an argument taken by our pipeline.py script.

## Dockerfile

A Dockerfile instantiates our docker image. We created it using the file:

```dockerfile
FROM python:3.9

RUN pip install pandas
RUN pip install pyarrow

WORKDIR /app
COPY pipeline.py pipeline.py

ENTRYPOINT [ "python", "pipeline.py" ]
```

where 'FROM' specifies the base docker image we will build on, 'RUN' sets up our image by installing prerequisites, 'WORKDIR' creates/specifies the working directory inside the container, 'COPY' copies the script to the container (first is source name, second is destination name) and 'ENTRYPOINT' defines what to do when the container runs.


## Basic pipeline

Our first pipeline will simply import the needed packages for our task, take an argument (as seen above) and print it. It is a very basic Python script to make sure everything is working.

```python
import sys
import pandas as pd

print(sys.argv)

day = sys.argv[1]

print(f"job finished successfully for day = {day}")
```