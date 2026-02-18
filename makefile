# Variables
VENV = venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

# Default target: build the venv and install requirements
.PHONY: install
install: $(VENV)/bin/activate

# Create venv if it doesn't exist; update if requirements.txt changes
$(VENV)/bin/activate: requirements.txt
	@echo "Creating virtual environment..."
	python3 -m venv $(VENV)
	@echo "Installing dependencies..."
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	touch $(VENV)/bin/activate

# Clean up the environment
.PHONY: clean
clean:
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -rf {} +

# Helper to run the app (optional)
.PHONY: run
run: install