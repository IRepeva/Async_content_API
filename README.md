# Project

Project contains 2 services:
## API

### Description
The API service provides access to information about all movies, persons, and genres. 
Films and persons can be searched by title, description and full name, respectively. 
Pagination and caching have been implemented to enhance the user experience.

For more detailed information about the service's endpoints, 
please visit [this link](http://0.0.0.0:8000/api/openapi) after starting the project 
using `docker-compose up -d`

## TESTS 
### Description
API tests were designed to verify that the API is functioning correctly and 
meeting its requirements

## Available make commands
 - `make run_app` - to run the API
 - `make run_tests` - to run all tests
 - `make logs_tests` - to see tests logs
