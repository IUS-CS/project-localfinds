# -------- OS DETECTION --------
WINDOWS ?= 0

ifeq ($(OS),Windows_NT)
    WINDOWS = 1
else
    WINDOWS = 0
endif

# -------- VARIABLES --------

VENV = venv
APP = src/localfinds/app.py

ifeq ($(WINDOWS),1)
	PYTHON = python
    PY = $(VENV)\Scripts\python
    PIP = $(VENV)\Scripts\pip
else
	PYTHON = python3
    PY = $(VENV)/bin/python3
    PIP = $(VENV)/bin/pip
endif

# -------- DEFAULT --------
all: run

# -------- ENV SETUP --------
venv:
	$(PYTHON) -m venv $(VENV)

install:
	$(PY) -m pip install --upgrade pip
	$(PY) -m pip install pytest
	$(PY) -m pip install flask

setup: venv install

# -------- RUN APP --------
run:
	$(PY) $(APP)

debug:
	FLASK_ENV=development $(PY) $(APP)

# -------- TESTS --------
test:
	$(PY) -m pytest -v

# -------- CLEAN --------
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -name "*.pyc" -delete
	rm -rf .pytest_cache

# -------- DB RESET --------
reset-db:
	rm -f src/database/posts.db