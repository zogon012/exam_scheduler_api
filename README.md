# Exam Scheduler API

This is a Django-based API for managing exam schedules and reservations. The application uses PostgreSQL as the database and is containerized using Docker and Docker Compose. Swagger is used for API documentation.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Running Tests](#running-tests)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Installation

### Prerequisites
- Docker
- Docker Compose

### Setup
1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/exam-scheduler-api.git
    cd exam-scheduler-api
    ```

2. Create a `.env` file in the root directory with the following content:
    ```env
    SECRET_KEY=your-secret-key
    DEBUG=True
    POSTGRES_DB=schedule
    POSTGRES_USER=admin
    POSTGRES_PASSWORD=password
    POSTGRES_HOST=db
    POSTGRES_PORT=5432
    ALLOWED_HOSTS=0.0.0.0,localhost,127.0.0.1
    ```

3. Build and start the containers:
    ```sh
    docker-compose up --build
    ```

4. Create a superuser for Django admin:
    ```sh
    docker-compose exec web python manage.py createsuperuser
    ```

## Usage

The application will be available at `http://0.0.0.0:8000/`. You can access the Django admin interface at `http://0.0.0.0:8000/admin/`.

Swagger documentation for the API can be accessed at `http://0.0.0.0:8000/swagger/`.

## Running Tests

To run tests, use the following command:
```sh
docker-compose exec web pytest --cov
```

## Configuration

### Environment Variables

The application configuration is managed through environment variables set in the `.env` file. Key variables include:

- `SECRET_KEY`: Django secret key
- `DEBUG`: Debug mode (set to `True` for development)
- `POSTGRES_DB`: Name of the PostgreSQL database
- `POSTGRES_USER`: PostgreSQL user
- `POSTGRES_PASSWORD`: PostgreSQL password
- `POSTGRES_HOST`: PostgreSQL host (set to `db` for Docker)
- `POSTGRES_PORT`: PostgreSQL port (default is `5432`)
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
