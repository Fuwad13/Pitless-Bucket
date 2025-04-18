help:
	@echo "Makefile for some common commands"

ngrok:
	ngrok http --url=promoted-cardinal-handy.ngrok-free.app 8000

pip-freeze:
	pip list --not-required --format=freeze > requirements.txt

alembic-revision:
	alembic revision --autogenerate -m "message here"

alembic-upgrade:
	alembic upgrade head

.PHONY: help ngrok pip pip-freeze alembic-revision alembic-upgrade