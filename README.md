# Nexa - Custom AI-Powered Alexa Skill

Nexa is a customizable, AI-powered Alexa skill using Python and Flask-Ask. It leverages artificial intelligence to enhance query processing and response generation, providing a sophisticated personal assistant experience. The name "Nexa" reflects the next generation of AI-powered assistants, emphasizing innovation and forward-thinking technology. This project offers a robust foundation for creating advanced skills with efficient request handling and scalable deployment.

## Table of Contents

- [Nexa - Custom AI-Powered Alexa Skill](#nexa---custom-ai-powered-alexa-skill)
  - [Table of Contents](#table-of-contents)
  - [Special Environment Requirements](#special-environment-requirements)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Command Line Arguments](#command-line-arguments)
    - [Examples](#examples)
  - [Configuration](#configuration)
  - [Shell Script](#shell-script)
    - [Shell Script Examples](#shell-script-examples)
    - [Running the Shell Script](#running-the-shell-script)
  - [Skill Testing](#skill-testing)
    - [Testing NexaIntent](#testing-nexaintent)
  - [License](#license)
    - [Notes:](#notes)

## Special Environment Requirements

To get this project to work, you need the following:
- Use Python version 3.9.6
- Install Flask-Ask from the specific GitHub commit using the following command:

```bash
pip install git+https://github.com/johnwheeler/flask-ask.git@8fa6aa052a8a4b5273cbcceb48e926b41dbe8a32
```

- Use Flask version 2.3.0.

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/kjpou1/nexa_ai.git
    cd nexa_ai
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set environment file**

    Copy or rename the `example_env` file to `.env` before running:

    ```bash
    cp example_env .env
    ```

## Usage

To run the Alexa skill, use the provided `run.py` script with appropriate command-line arguments.

### Command Line Arguments

The following command-line arguments can be used:

- `--server` or `-s`: Specify the server host (default: `0.0.0.0`).
- `--port` or `-p`: Specify the server port (default: `8045`).
- `--intent` or `-i`: Specify the intent name to be handled dynamically (default: `NexaIntent`).

### Examples

To run the program with default settings:

```bash
python run.py
```

To run the program with a specified host, port, and intent:

```bash
python run.py --server 0.0.0.0 --port 8045 --intent NexaIntent
```

## Configuration

The configuration settings are managed through environment variables and can be set in a `.env` file in the root directory of the project. 

Example `.env` file:

``` 
SERVER_HOST=0.0.0.0
SERVER_PORT=8045
INTENT=NexaIntent
DEBUG=True
```

> [!NOTE]
> An `example_env` file is provided to get started. Copy the file to `.env` before running:

```bash
cp example_env .env
```

## Shell Script

A shell script `run.sh` is provided to automate the execution of the script.

### Shell Script Examples

Example `run.sh`

```bash
#!/bin/bash
source ./.venv/bin/activate
python ./run.py
deactivate
```

### Running the Shell Script

To run the script:

```bash
./run.sh
```

## Skill Testing

### Testing NexaIntent

To test the dynamically specified intent, you can use the Alexa Developer Console. 

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

### Notes:

1. **Environment Configuration**: The `.env` file should reflect all environment variables used within the project.

---