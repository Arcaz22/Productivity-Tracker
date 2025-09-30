# Productivity Tracker API

## Feature
- Authentication Keycloak
- Manage User
- RBAC (Role Based Access Control)
- Integration with PostgreSQL

## Config Docker
1. Run Docker:
   ```sh
   docker run -d \
     --name keycloak \
     -p 9999:8080 \
     -e KEYCLOAK_ADMIN=keycloak \
     -e KEYCLOAK_ADMIN_PASSWORD=password \
     quay.io/keycloak/keycloak:26.0 \
     start-dev

## Installation
1. Run keycloak:
   ```sh
   docker start keycloak
   ```
2. Install dependencies:
   ```sh
   uv sync
   ```
3. Copy `.env.example` to `.env`
4. Migrate database:
   ```sh
   alembic upgrade head
   ```
5. Run App:
   ```sh
   uv run fastapi dev
   ```
