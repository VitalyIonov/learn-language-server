start:
	docker compose up

db-connect:
	docker exec -it postgres-db psql -U postgres -d app

db-migrate-gen:
	docker compose run --rm web bash -lc 'PYTHONPATH=. alembic revision --autogenerate' && git add 'app/db/migrations'

db-migrate:
	docker compose run --rm web sh -lc 'PYTHONPATH=. poetry run alembic upgrade head'

db-seed:
	docker compose run --rm web sh -lc 'PYTHONPATH=. python app/seed.py'

reset-db:
	docker exec -i learn-language-db-1 psql -U postgres -d app -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"