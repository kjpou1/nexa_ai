# Docker Documentation for basic_rest_api_template
- [Docker Documentation for basic\_rest\_api\_template](#docker-documentation-for-basic_rest_api_template)
  - [Directory Structure](#directory-structure)
    - [Files Overview](#files-overview)
  - [Building and Running the Docker Container](#building-and-running-the-docker-container)
    - [Prerequisites](#prerequisites)
    - [Using Docker Compose](#using-docker-compose)
      - [Step-by-Step Guide](#step-by-step-guide)
      - [Example Docker Compose File (`docker-compose.yml`)](#example-docker-compose-file-docker-composeyml)
      - [Custom Docker Compose File (`local_docker-compose.yml`)](#custom-docker-compose-file-local_docker-composeyml)
    - [Building and Using the Docker Image Directly](#building-and-using-the-docker-image-directly)
      - [Example of a Customized Command Line](#example-of-a-customized-command-line)
  - [Common Docker Commands](#common-docker-commands)
    - [Building the Docker Image](#building-the-docker-image)
    - [Running the Docker Container](#running-the-docker-container)
    - [Stopping the Docker Container](#stopping-the-docker-container)
    - [Viewing Logs](#viewing-logs)
    - [Inspecting the Container](#inspecting-the-container)
  - [Troubleshooting](#troubleshooting)
    - [Container Fails to Start](#container-fails-to-start)
    - [File Not Found Errors](#file-not-found-errors)
  - [Conclusion](#conclusion)

This document provides instructions for building, running, and managing the Docker containers for the `basic_rest_api_template` project.

## Directory Structure

The following files are located in the `deployments/` directory:

```
deployments/
├── Dockerfile
├── docker-compose.yml
└── .dockerignore
```

### Files Overview

- **Dockerfile**: Defines the Docker image for the project.
- **docker-compose.yml**: Example Docker Compose file that can be copied and modified to run the application on a local machine.
- **.dockerignore**: Specifies which files and directories should be ignored by Docker.

## Building and Running the Docker Container

### Prerequisites

Ensure you have Docker and Docker Compose installed on your machine.

### Using Docker Compose

#### Step-by-Step Guide

1. **Navigate to the Project Directory**

   Navigate to the root directory of your project:

   ```bash
   cd /path/to/your/project
   ```

2. **Copy the Example Docker Compose File**

   Copy the example `docker-compose.yml` file to `deployments/local_docker-compose.yml` for your local environment setup:

   ```bash
   cp deployments/docker-compose.yml deployments/local_docker-compose.yml
   ```

3. **Modify the `local_docker-compose.yml` File**

   Open `deployments/local_docker-compose.yml` and modify it to suit your local environment. Ensure the paths are correctly set for your local data and configuration files.

4. **Build the Docker Image**

   Use the `--build` flag with `docker-compose up` to rebuild the image:

   ```bash
   docker-compose -f deployments/local_docker-compose.yml up --build -d
   ```

#### Example Docker Compose File (`docker-compose.yml`)

This is an example Docker Compose file that you can copy and modify to run the application on your local machine.

```yaml
services:
  basic_rest_api_template:
    container_name: basic_rest_api_container
    build:
      context: ..
      dockerfile: ./deployments/Dockerfile
    ports:
      - "8080:8080"
    environment:
      FLASK_APP: run.py
      FLASK_RUN_HOST: 0.0.0.0
    volumes:
      - ..:/usr/src/app
    command: ["python", "run.py"]
```

#### Custom Docker Compose File (`local_docker-compose.yml`)

This Docker Compose file is used to run the local server. It is customized for my local development environment.

```yaml
services:
  basic_rest_api_template:
    container_name: basic_rest_api_container
    build:
      context: ..
      dockerfile: ./deployments/Dockerfile
    ports:
      - "8080:8080"
    environment:
      FLASK_APP: run.py
      FLASK_RUN_HOST: 0.0.0.0
    volumes:
      - ..:/usr/src/app
    command: ["python", "run.py"]
```

### Building and Using the Docker Image Directly

If you prefer to build and run the Docker container directly without using Docker Compose, follow these steps:

1. **Navigate to the Project Directory**

   Navigate to the root directory of your project:

   ```bash
   cd /path/to/your/project
   ```

2. **Build the Docker Image**

   Use the following command to build the Docker image:

   ```bash
   docker build -f ./deployments/Dockerfile -t basic_rest_api_template .
   ```

3. **Remove Any Existing Container**

   If there's already a container running with the same name, remove it:

   ```bash
   docker rm -f basic_rest_api_container
   ```

4. **Run the Docker Container**

   Use the following command to run the Docker container:

   ```bash
   docker run -d -p 8080:8080 --name basic_rest_api_container basic_rest_api_template
   ```

#### Example of a Customized Command Line

Here is an example command customized for specific local paths:

```bash
docker run -d -p 8080:8080 --name basic_rest_api_container basic_rest_api_template
```

## Common Docker Commands

### Building the Docker Image

To build the Docker image, use the following command:

```bash
docker-compose -f deployments/local_docker-compose.yml build
```

### Running the Docker Container

To run the Docker container, use the following command:

```bash
docker-compose -f deployments/local_docker-compose.yml up -d
```

### Stopping the Docker Container

To stop the Docker container, use the following command:

```bash
docker-compose -f deployments/local_docker-compose.yml down
```

### Viewing Logs

To view the logs of the running container, use the following command:

```bash
docker logs basic_rest_api_template
```

### Inspecting the Container

To inspect the container and verify volume mounts, use the following command:

```bash
docker inspect basic_rest_api_template
```

## Troubleshooting

### Container Fails to Start

If the container fails to start, check the logs for error messages:

```bash
docker logs basic_rest_api_template
```

### File Not Found Errors

Ensure that the paths in the `docker-compose.yml` file are correct and that the files exist at those locations.

## Conclusion

This document provides the necessary steps to build, run, and manage Docker containers for the `basic_rest_api_template` project. If you encounter any issues, refer to the troubleshooting section or check the Docker logs for more details.