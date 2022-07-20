run_tests:
	docker-compose -f docker-compose.test.yml --env-file ./tests/functional/.env.test up -d --build

run_app:
	docker-compose -f docker-compose.yml up -d --build

down:
	docker-compose down

logs_tests:
	docker-compose logs -f tests
