# How to Deploy the Block Planner

This guide walks you through deploying the full Railway Block Planner stack using Docker.

## Prerequisites

- **Docker**: Version 20.10+
- **Docker Compose**: Version 2.0+
- **Hardware**: Minimum 4GB RAM (OR-Tools can be memory-intensive).

## Steps

### 1. Clone the Repository
```bash
git clone git@github.com:rehaan-ahmad/GIGO-SIH-2026.git
cd GIGO
```

### 2. Configure Environment
Create a `.env` file in the root directory. You can copy the example:
```bash
cp .env.example .env
```
Edit `.env` to set your database credentials if you are not using the defaults.

### 3. Launch the Stack
Run the compose command to build and start all containers:
```bash
docker-compose up --build -d
```

### 4. Verify Deployment
Check if the containers are running:
```bash
docker-compose ps
```
You should see the `backend`, `frontend`, `redis`, and `db` containers in the `Up` state.

## Verification

- **Frontend**: Open `http://localhost` in your browser. You should see the Dashboard.
- **Backend**: Visit `http://localhost:8000/docs` to access the Swagger UI.
- **Database**: Ensure the `db` container is running. The backend will automatically initialize the PostGIS extension on startup.

## Troubleshooting

| Issue | Fix |
| :--- | :--- |
| **Port 80 Conflict** | Change the frontend port mapping in `docker-compose.yml` from `80:80` to `8080:80`. |
| **DB Connection Failed** | Ensure the `db` container has fully started before the `backend` tries to connect. Run `docker-compose restart backend`. |
| **OR-Tools Memory Error** | Increase the Docker Desktop memory limit to 8GB in Settings $\rightarrow$ Resources. |
