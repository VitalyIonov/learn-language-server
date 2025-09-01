start:
	docker compose up

db-connect:
	docker exec -it postgres-db psql -U postgres -d app

db-migrate-gen:
	docker compose run --rm web bash -lc 'PYTHONPATH=. alembic revision --autogenerate'

db-migrate:
	docker compose run --rm web sh -lc 'PYTHONPATH=. poetry run alembic upgrade head'

db-seed:
	PYTHONPATH=. poetry run python app/seed.py

reset-db:
	docker exec -i learn-language-db-1 psql -U postgres -d app -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"