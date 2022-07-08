logs_tests:
	docker-compose -f tests/functional/docker-compose.yml logs -f $(c)

logs_api:
	docker-compose logs -f $(c)

down_tests:
	docker-compose -f tests/functional/docker-compose.yml --env-file tests/functional/.env down

down_api:
	docker-compose down

run_tests:
	docker-compose -f tests/functional/docker-compose.yml --env-file tests/functional/.env up -d

run_api:
	docker-compose up -d

tests:
	pytest src -svvv -rs api/v1