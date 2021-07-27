# Docker Flask API Example

## Steps to update the docker image and to run it locally

1. Clone the repository

```bash
git clone git@github.com:gennsev/FlaskAPI_Docker_example.git
cd service
```

2. Build and tag the image

```bash
docker build -t docker_example .
```

3. Run the image locally

```bash
docker run -p 8000:8000 docker_example
```
