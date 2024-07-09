# BASIC_ALEXA_SKILL_TEMPLATE

This is a foundational Python template for developing Alexa skills using Flask-Ask.

> [!NOTE] 
> To get this project to work, you need the following:
> - use Python version 3.9.6
> - install Flask-Ask from the specific GitHub commit using the following command:
> 
> ```bash
> pip install git+https://github.com/johnwheeler/flask-ask.git@8fa6aa052a8a4b5273cbcceb48e926b41dbe8a32
> ```
> 
> - use Flask version 2.3.0.

## Table of Contents

- [BASIC\_ALEXA\_SKILL\_TEMPLATE](#basic_alexa_skill_template)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Command Line Arguments](#command-line-arguments)
    - [Examples](#examples)
  - [Configuration](#configuration)
  - [Shell Script](#shell-script)
    - [Shell Script Examples](#shell-script-examples)
    - [Running the Shell Script](#running-the-shell-script)
  - [Skill Testing](#skill-testing)
    - [Testing MyCustomIntent](#testing-mycustomintent)
  - [License](#license)
    - [Notes:](#notes)

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/project_name.git
    cd project_name
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

- `--server` or `-s`: Specify the server host (default: `127.0.0.1`).
- `--port` or `-p`: Specify the server port (default: `5000`).
- `--intent` or `-i`: Specify the intent name to be handled dynamically (default: `MyCustomIntent`).

### Examples

To run the program with default settings:

```bash
python run.py
```

To run the program with a specified host, port, and intent:

```bash
python run.py --server 127.0.0.1 --port 5000 --intent MyCustomIntent
```

## Configuration

The configuration settings are managed through environment variables and can be set in a `.env` file in the root directory of the project. 

Example `.env` file:

``` 
SERVER_HOST=127.0.0.1
SERVER_PORT=5000
INTENT=MyCustomIntent
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

### Testing MyCustomIntent

To test the dynamically specified intent, you can use the Alexa Developer Console. 

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

### Notes:

1. **Project Name**: Ensure to replace `project_name` with the actual name of your project in the clone command.
2. **Intent Testing**: The curl command and example response are illustrative. Actual testing may require interaction with the Alexa developer console or an Alexa-enabled device.
3. **Environment Configuration**: The `.env` file should reflect all environment variables used within the project.
