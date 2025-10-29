# LLM-Computer_Vision

## Overview

This project integrates Large Language Models (LLMs) with computer vision tasks, enabling intelligent planning and execution of complex visual analysis workflows. It features a modular architecture with a FastAPI backend, a dedicated executor for vision tasks, an LLM-driven planner, and a React-based user interface. The system is designed to interpret high-level natural language requests, break them down into actionable computer vision steps, execute them, and present the results.

## Features

*   **LLM-Powered Planning:** Utilizes Large Language Models to generate dynamic execution plans for computer vision tasks based on natural language input.
*   **Modular Architecture:** Separates concerns into distinct services:
    *   **Backend:** Manages API requests, job queues, artifact storage, and overall system orchestration.
    *   **Planner:** Responsible for interpreting user requests and generating execution plans.
    *   **Executor:** Executes the steps defined by the planner, interacting with computer vision models and tools.
    *   **UI:** Provides an intuitive web interface for users to submit tasks, monitor progress, and view results.
*   **Containerized Deployment:** Leverages Docker and Docker Compose for easy setup, deployment, and scalability.
*   **Shared DSL:** Defines a Domain Specific Language (DSL) for consistent communication and data modeling across services.
*   **Health Monitoring:** Includes API endpoints for checking the health and status of various services.

## Technologies Used

*   **Backend:** Python, FastAPI
*   **Frontend:** React, TypeScript, Vite
*   **LLM Integration:** (Specific LLM framework/library would go here, e.g., LangChain, LlamaIndex, custom integration)
*   **Computer Vision:** (Specific CV libraries/frameworks would go here, e.g., OpenCV, PyTorch, TensorFlow, Hugging Face Transformers)
*   **Containerization:** Docker, Docker Compose
*   **Package Management:** `pyproject.toml` (Poetry/PDM) for Python, `npm`/`yarn` for Node.js
*   **Styling:** CSS

## Setup and Installation

This project uses Docker Compose for a streamlined setup.

### Prerequisites

*   Docker Desktop (or Docker Engine and Docker Compose) installed on your system.

### Steps

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/kowsik11/LLM-Computer_Vision.git
    cd LLM-Computer_Vision
    ```

2.  **Build and run the services:**
    Navigate to the `infra` directory and start the services using Docker Compose:
    ```bash
    cd infra
    docker-compose up --build -d
    ```
    This command will:
    *   Build Docker images for the `backend`, `executor`, `planner`, and `ui` services.
    *   Start all services in detached mode (`-d`).

3.  **Access the UI:**
    Once all services are up and running, you can access the web interface (UI) in your browser, typically at:
    `http://localhost:3000` (or the port configured in `ui/vite.config.ts` and `infra/docker-compose.yml`).

4.  **Stop the services:**
    To stop and remove the running containers, networks, and volumes:
    ```bash
    cd infra
    docker-compose down
    ```

## Project Structure

```
.
├── backend/              # FastAPI backend for API, job management, artifacts
│   ├── app/              # Main application code
│   ├── Dockerfile        # Dockerfile for backend service
│   └── pyproject.toml    # Python dependencies
├── docs/                 # Project documentation
├── executor/             # Service for executing computer vision tasks
│   ├── executor/         # Executor application code
│   ├── Dockerfile        # Dockerfile for executor service
│   └── pyproject.toml    # Python dependencies
├── infra/                # Infrastructure setup (Docker Compose)
│   └── docker-compose.yml# Defines multi-service Docker application
├── planner/              # LLM-driven planning service
│   ├── planner/          # Planner application code
│   ├── Dockerfile        # Dockerfile for planner service
│   └── pyproject.toml    # Python dependencies
├── shared/               # Shared Domain Specific Language (DSL) models and schemas
│   ├── dsl/              # DSL definitions
│   └── pyproject.toml    # Python dependencies
├── ui/                   # React/TypeScript frontend
│   ├── src/              # Frontend source code
│   ├── Dockerfile        # Dockerfile for UI service
│   └── package.json      # Node.js dependencies
└── README.md             # This file
```

## Usage

(Detailed instructions on how to use the application, e.g., submitting a task via the UI, example natural language prompts, expected outputs.)

## Contributing

We welcome contributions! Please see our `CONTRIBUTING.md` (if available) for guidelines on how to contribute to this project.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
