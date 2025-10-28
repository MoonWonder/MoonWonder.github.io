PYTHON ?= python3
VENV ?= .venv
AUDIT_SCRIPT := scripts/content_audit.py
REPORTS_DIR ?= reports
AUDIT_ARGS ?=

.PHONY: audit clean-venv

$(VENV)/bin/python: requirements.txt
	$(PYTHON) -m venv $(VENV)
	$(VENV)/bin/python -m pip install --upgrade pip
	$(VENV)/bin/python -m pip install -r requirements.txt

audit: $(VENV)/bin/python
	$(VENV)/bin/python $(AUDIT_SCRIPT) --reports-dir $(REPORTS_DIR) $(AUDIT_ARGS)

clean-venv:
	rm -rf $(VENV)
