run-api:
	make stop-all
	docker-compose up -d --build

run-database:
	make stop-all
	docker-compose up -d mongo-db

stop-all:
	docker-compose down