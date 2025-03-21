# Chat API

A robust Chat REST API built with FastAPI, following the Domain-Driven Design (DDD) pattern. This project is
containerized using Docker, employs GitHub Actions for continuous integration, integrates Loki for centralized logging,
and utilizes a Makefile for streamlined project management.

## Features

- **FastAPI**: High-performance web framework for building APIs with Python 3.13.
- **Domain-Driven Design (DDD)**: Structured approach to software design that emphasizes domain modeling.
- **MongoDB & Mongo Express**: NoSQL database for storing chat data, with a web-based MongoDB admin interface.
- **Nginx**: Reverse proxy server for handling client requests.
- **Loki**: Centralized logging system integrated for log aggregation and monitoring.
- **Pre-commit Hooks**: Code quality tools including flake8, autoflake, add-trailing-comma, and isort.
- **Mypy**: Static type checker for Python.
- **GitHub Actions**: Automated workflows for testing and formatting on each push and pull request.
- **Docker & Docker Compose**: Containerization for easy setup and deployment.
- **Makefile**: Simplifies common tasks such as setup, testing, and running the application.
- **Optimized Docker Image**: Reduced FastAPI Docker image size from 700MB to 205MB for development container
  and 185MB for production container by implementing multi-stage builds.

**Note:** Each service (loggers, servers, app, storages) is configured in its own Docker Compose file. This modular
setup ensures optimal performance and easier troubleshooting, reducing potential conflicts.

## Table of Contents

- [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Running the Application](#running-the-application)
- [Makefile Commands](#makefile-commands)
- [Docker](#docker)
- [Project Structure](#project-structure)
- [Health Check Endpoint](#health-check-endpoint)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Getting Started

### Prerequisites

Ensure you have the following installed:

- [Docker](https://www.docker.com/get-started)
- **Makefile Execution Requirements**: Ensure that `make` is installed on your system. Most UNIX-like systems have it
  pre-installed.

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
3. **Run Make Commands**:

   It will start the app, just FastAPI application:

   ```bash
   make app
   ```

### Running the Application

The project includes a `Makefile` for simplified management. Refer to the [Makefile Commands](#makefile-commands)
section for details.

## Makefile Commands

The `Makefile` provides a set of commands to manage and run various parts of the application:

### Usage Examples

- **Start All Services - Development**:
  ```bash
  make all
  ```
  Starts the application, storages, server, and loggers in **_development_** mode.


- **Start All Services - Production**:
  ```bash
  make all-prod
  ```
  Starts the application, storages, server, and loggers in **_production_** mode.


- **Start Only the Application - Development**:
  ```bash
  make app
  ```
  Starts the main application container - FastAPI in **_development_** mode.


- **Start Only the Application - Production**:
  ```bash
  make app-prod
  ```
  Starts the main application container - FastAPI in **_production_** mode.


- **Start the Server**:
  ```bash
  make server
  ```
  Starts the Nginx server, which serves as a reverse proxy.
-

- **Start Storages**:
  ```bash
  make storages
  ```
  Starts MongoDB and Mongo Express. Mongo Express can be accessed at [http://localhost:28081](http://localhost:28081).


- **Start Storages Without Admin Interface - MongoExpress**:
  ```bash
  make storages-pure
  ```
  Starts _**only**_ MongoDB.


- **Start Loggers**:
  ```bash
  make loggers
  ```
  Builds and starts Loki and Grafana for centralized logging and monitoring.


- **Stop the Application - Development**:
  ```bash
  make app-down
  ```
  Stops the application container.


- **Stop the Application - Production**:
  ```bash
  make app-prod-down
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


- **Stop Storages**:
  ```bash
  make storages-pure-down
  ```
  Stops MongoDB without erasing data.


- **Stop All Services - Development**:
  ```bash
  make all-down
  ```
  Stops all running services.


- **Stop All Services - Production**:
  ```bash
  make all-prod-down
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

---

## **Docker**

This project includes Docker configurations for both **development** and **production** environments. The Docker images
are built using two different Dockerfiles, `dev.Dockerfile` for development and `prod.Dockerfile` for production, with
the configuration driven by environment variables defined in `.env` files.

### **Dockerfiles Overview**

- **`prod.Dockerfile`**: Used for building the Docker image in the **production** environment. It runs with **Gunicorn**
  and **UvicornWorker** for handling multiple requests efficiently in a production setting. No file watching or
  reloading is enabled. This environment only includes the **production dependencies**, ensuring a minimal and optimized
  setup for performance.

- **`dev.Dockerfile`**: Used for building the Docker image in the **development** environment. It runs with **Uvicorn**
  in **reload mode** and is configured to watch file changes, making it suitable for active development. In this
  environment, **development dependencies** (including testing tools like `pytest`) are installed, allowing you to run
  tests and develop in an interactive manner.

### **Environment Configuration**

- The **environment files** (`.env`, `.env.prod`) are used to provide dynamic configuration based on the environment.

### **Makefile Commands**

- **`make app-prod`**:
  Builds and runs the production environment by using `.env.prod` for configuration. The app will run with **Gunicorn**(
  without reloading or volume watching) to handle production-level traffic. It uses **only production dependencies**,
  ensuring a lightweight and optimized container.

  ```bash
  make app-prod
  ```

- **`make app`**:
  Builds and runs the development environment by using `.env` for configuration. The app will run with **Uvicorn** in
  *reload mode*, allowing live code reloading and volume watching for a smoother development experience. In this
  environment, **development dependencies** are installed, including tools like `pytest` for testing purposes. This
  setup allows you to perform tests within the development container, not in production.

  ```bash
  make app
  ```

---

## Project Structure

```plaintext
📦 chat-api
├── 📂 .github
│   └── 📂 workflows
│       └── 📄 ci.yml          # GitHub Actions CI workflow
├── 📂 app
│   ├── 📂 application
│   ├── 📂 domain
│   ├── 📂 infra
│   ├── 📂 logic
│   ├── 📂 settings
│   ├── 📂 tests
│   ├── 📂 utils
├── 📂 config
│   └── 📄 loki-config.yaml     # Configuration for Loki logger
│   └── 📄 nginx.yaml           # Configuration for Nginx logger
│   └── 📄 protmail-config.yaml # Configuration for Protmail logger
├── 📂 docker_compose
│   ├── 📄 app.yaml             # Main App
│   └── 📄 loggers.yml          # Loggers - Protmail, Granafa and Loki
│   └── 📄 server.yml           # Proxy Server - Nginx
│   └── 📄 storages.yml         # Storages - Mongo DB
│   └── 📄 storages_ui.yml      # Storages Admin Interface - Mongo Express
.
.
.
├── 📄 .pre-commit-config.yaml  # Pre-commit hooks configuration
├── 📄 Dockerfile
├── 📄 Makefile
├── 📄 mypy.ini                 # MyPy configuration
├── 📄 pyproject.toml           # Python project configuration
├── 📄 ruff.toml                # Ruff linter configuration
└── 📄 uv.lock                  # UV dependency lock file
```

---

## **Health Check Endpoint**

The application includes a **health check endpoint** to monitor the system's overall status, specifically the health of
the **MongoDB** connection. The health check is provided through a dedicated router, which can be queried to determine
whether the system and MongoDB are running properly.

### **Endpoint: `/health`**

- **Method**: `GET`
- **Tags**: Health
- **Response Model**: `HealthOut` (custom schema for structured health check response)
- **Description**: This endpoint performs a system-wide health check, including verifying MongoDB's availability by
  attempting to ping the database.

### **How It Works**:

- The health check route is defined in the `Health` router.
- The system attempts to **ping MongoDB** using the `mongo_db_client` to ensure that the database is up and running.
- If MongoDB responds successfully, the status is considered healthy, and the system will return a `healthy` status with
  detailed MongoDB health info.
- If MongoDB is not available or an error occurs during the ping, the system will return a status indicating that
  MongoDB is down and provide the error details.

### **Example Response:**

```json
{
  "status": "healthy",
  "detail": {
    "mongodb": "Ok"
  }
}
```

If MongoDB is unavailable:

```json
{
  "status": "MongoDB is down",
  "detail": {
    "mongodb": "error: <error_message>"
  }
}
```

### **Usage**:

- This endpoint can be used to monitor the health of the application, especially MongoDB.
- Typically, it can be integrated into **monitoring tools** or queried periodically to ensure the system is functioning
  correctly.

_This endpoint ensures that the core components of your system are functioning and allows for efficient monitoring and
troubleshooting._

## API Endpoints

The Chat API provides the following endpoints:

- **Chats**:
    - `POST /chat/`: Create a new chat.
    - `POST /chat/{chat_oid}/message`: Send a message in a chat.
- **Health**:
    - `Get /Health/`: health check.

For detailed request and response schemas, refer to the [API Documentation](http://localhost:8000/api/docs).

## Testing

The project includes extensive testing capabilities, designed to validate business logic independently of the database.
This ensures that core functionalities can be tested efficiently without requiring a connection to MongoDB or other
external services.

- **Unit Tests**: Focused on individual components, testing business logic in isolation.
- **Integration Tests**: Verify that different parts of the system work together as expected.
- **Database-Free Testing**: The architecture allows for testing business logic independently of the database. Mocking
  or in-memory databases can be used to simulate data operations.

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
