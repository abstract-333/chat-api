# Chat API
![Build Status](https://img.shields.io/github/workflow/status/abstract-333/chat-api/CI?label=build)
![Test Coverage](https://coveralls.io/repos/github/abstract-333/chat-api/badge.svg)

A robust Chat REST API built with FastAPI, following the Domain-Driven Design (DDD) pattern. This project is containerized using Docker, employs GitHub Actions for continuous integration, integrates Loki for centralized logging, and utilizes a Makefile for streamlined project management.

## Features

- **FastAPI**: High-performance web framework for building APIs with Python 3.12.
- **Domain-Driven Design (DDD)**: Structured approach to software design that emphasizes domain modeling.
- **MongoDB & Mongo Express**: NoSQL database for storing chat data, with a web-based MongoDB admin interface.
- **Nginx**: Reverse proxy server for handling client requests.
- **Loki**: Centralized logging system integrated for log aggregation and monitoring.
- **Pre-commit Hooks**: Code quality tools including flake8, autoflake, add-trailing-comma, and isort.
- **Mypy**: Static type checker for Python.
- **GitHub Actions**: Automated workflows for testing and formatting on each push and pull request.
- **Docker & Docker Compose**: Containerization for easy setup and deployment.
- **Makefile**: Simplifies common tasks such as setup, testing, and running the application.
- **Optimized Docker Image**: Reduced FastAPI Docker image size from 700MB to 200MB by implementing multi-stage builds.

**Note:** Each service (loggers, servers, app, storages) is configured in its own Docker Compose file. This modular setup ensures optimal performance and easier troubleshooting, reducing potential conflicts.
## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
- [Makefile Commands](#makefile-commands)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Getting Started

### Prerequisites

Ensure you have the following installed:

- [Docker](https://www.docker.com/get-started)
- **Makefile Execution Requirements**: Ensure that `make` is installed on your system. Most UNIX-like systems have it pre-installed.

### Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/abstract-333/chat-api.git
   cd chat-api
   ```

2. **Set Up Environment Variables**:

   Copy the example environment variables file and modify as needed:

   ```bash
   cp .env.example .env
   ```

   Ensure to set the appropriate values in the `.env` file.

### Running the Application

The project includes a `Makefile` for simplified management. Refer to the [Makefile Commands](#makefile-commands) section for details.

## Makefile Commands

The `Makefile` provides a set of commands to manage and run various parts of the application:

### Usage Examples

- **Start All Services**:
  ```bash
  make all
  ```
  Starts the application, storages, server, and loggers.

- **Start Only the Application**:
  ```bash
  make app
  ```
  Starts the main application container.

- **Start the Server**:
  ```bash
  make server
  ```
  Starts the Nginx server, which serves as a reverse proxy.

- **Start Storages**:
  ```bash
  make storages
  ```
  Starts MongoDB and Mongo Express. Mongo Express can be accessed at [http://localhost:28081](http://localhost:28081).

- **Start Loggers**:
  ```bash
  make loggers
  ```
  Builds and starts Loki and Grafana for centralized logging and monitoring.

- **Stop the Application**:
  ```bash
  make app-down
  ```
  Stops the application container.

- **Stop the Server**:
  ```bash
  make server-down
  ```
  Stops the Nginx server.

- **Stop Loggers**:
  ```bash
  make loggers-down
  ```
  Stops Loki and Grafana.

- **Stop Storages**:
  ```bash
  make storages-down
  ```
  Stops MongoDB and Mongo Express without erasing data.

- **Stop All Services**:
  ```bash
  make all-down
  ```
  Stops all running services.

- **View Application Logs**:
  ```bash
  make app-logs
  ```
  Displays logs from the application container.

- **Run Tests**:
  ```bash
  make test
  ```
  Executes the test suite.

## Project Structure

```plaintext
chat-api/
├── app/
│   ├── api/                # API routes
│   ├── core/               # Core settings and configurations
│   ├── models/             # Database models
│   ├── repositories/       # Data access layer
│   ├── services/           # Business logic
│   ├── main.py             # Application entry point
│   └── ...
├── config/
│   ├── nginx/
│   └── ...
├── docker_compose/
│   ├── docker-compose.yml  # Docker Compose configuration
│   └── ...
├── tests/
│   ├── ...
├── .env.example            # Example environment variables
├── Dockerfile              # Docker build file
├── Makefile                # Makefile for managing tasks
├── README.md               # Project documentation
└── ...
```


## API Endpoints

The Chat API provides the following endpoints:

- **Authentication**:
  - `POST /auth/login`: Authenticate a user and receive a token.
  - `POST /auth/register`: Register a new user.

- **Users**:
  - `GET /users/`: Retrieve a list of users.
  - `GET /users/{user_id}`: Retrieve a specific user by ID.

- **Chats**:
  - `POST /chats/`: Create a new chat.
  - `GET /chats/{chat_id}`: Retrieve a specific chat by ID.
  - `POST /chats/{chat_id}/messages`: Send a message in a chat.
  - `GET /chats/{chat_id}/messages`: Retrieve messages from a chat.


For detailed request and response schemas, refer to the [API Documentation](http://localhost:8000/docs).

## Testing

The project includes extensive testing capabilities, designed to validate business logic independently of the database. This ensures that core functionalities can be tested efficiently without requiring a connection to MongoDB or other external services.

- **Unit Tests**: Focused on individual components, testing business logic in isolation.
- **Integration Tests**: Verify that different parts of the system work together as expected.
- **Database-Free Testing**: The architecture allows for testing business logic independently of the database. Mocking or in-memory databases can be used to simulate data operations.

Run the test suite with:

```bash
make test
```

Ensure that all tests pass before committing new code.

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the Repository**: Click the 'Fork' button at the top right of this page.
2. **Clone Your Fork**:

   ```bash
   git clone https://github.com/your-username/chat-api.git
   cd chat-api
   ```

3. **Create a Branch**:

   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make Changes**: Implement your feature or bug fix.
5. **Run Tests**: Ensure all tests pass.
6. **Commit Changes**:

   ```bash
   git commit -m "Add feature: your feature name"
   ```

7. **Push to GitHub**:

   ```bash
   git push origin feature/your-feature-name
   ```

8. **Create a Pull Request**: Navigate to your fork on GitHub and create a pull request to the main repository.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

