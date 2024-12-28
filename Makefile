# Docker Compose Management
up:
	docker compose up -d

stop:
	@docker compose stop

down:
	@docker compose down

build:
	@docker compose build

# Database Management
db_create_migrations:
	@docker compose exec web python manage.py makemigrations

db_empty_cbam_migration:
	@docker compose exec web python manage.py makemigrations cbam --empty

db_migrate:
	@docker compose exec web python manage.py migrate

db_sync: db_create_migrations db_migrate

db_dump:
	docker exec -it cbam_db sh -c 'pg_dump -U postgres -f /tmp/dbdump -Fc --no-acl --no-owner -Z 9 postgres'
	docker cp cbam_db:/tmp/dbdump dbdump

db_restore:
	@docker compose down
	@docker volume rm cbam_postgres_volume
	@docker compose up -d
	@echo Waiting 5 seconds
	@sleep 5
	docker cp dbdump cbam_db:/tmp/dbdump
	docker exec -it cbam_db sh -c 'pg_restore -U postgres -d postgres /tmp/dbdump'

db_clean:
	@docker compose down
	@docker volume rm cbam_postgres_volume

db_psql:
	@docker compose exec db psql "user=postgres"

# Other Commands
bash:
	@docker compose exec web bash

bash_no_run:
	@docker compose run --rm web bash

django_shell:
	@docker compose exec web python manage.py shell

create_superuser:
	@docker compose exec web python manage.py createsuperuser

collectstatic:
	@docker compose exec web python manage.py collectstatic --clear

send_reminders:
	@docker compose exec web python manage.py send_reminders
