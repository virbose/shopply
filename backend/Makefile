# Makefile

.PHONY: resetdb migrate loaddata

resetdb:
	rm -f db.sqlite3

migrate:
	pipenv run python manage.py makemigrations
	pipenv run python manage.py migrate

loaddata:
	pipenv run python manage.py loaddata backend/customers/customers.json
	pipenv run python manage.py loaddata backend/products/products.json

rebuild: resetdb migrate loaddata
setupdb: migrate loaddata