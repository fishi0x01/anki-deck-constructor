VENV := .venv/bin/activate

venv:
	@rm -rf .venv
	@python -m venv .venv
	@. $(VENV) && pip install --upgrade pip
	@. $(VENV) && pip install -r requirements.txt	

run:
	@mkdir -p media
	@rm -f media/*
	@rm -f collection.apkg
	@. $(VENV) && python main.py
