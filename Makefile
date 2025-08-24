start:
	docker compose up

db-connect:
	docker exec -it postgres-db psql -U postgres -d app

db-migrate-gen:
	PYTHONPATH=. poetry run alembic revision --autogenerate

db-migrate:
	PYTHONPATH=. poetry run alembic upgrade head

db-seed:
	PYTHONPATH=. poetry run python app/seed.py

reset-db:
	docker exec -i postgres-db psql -U postgres -d app -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"