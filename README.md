ETL Pipeline in Docker

Overview


This project is an ETL (Extract, Transform, Load) pipeline that fetches data from a public API, processes it, and stores it in PostgreSQL while also saving raw and transformed data locally for persistency.

Features

Extracts data from the Random User API every 30 seconds

Stores raw data in PostgreSQL and local JSON files

Transforms data into a structured format

Saves transformed data in local JSON files

Logs ETL execution details

Runs in a Docker container with mounted volumes for persistency

Prerequisites

Docker installed on your machine

PostgreSQL instance running (can be local or cloud-based)

Setup and Installation

1. Build the Docker Image

docker build -t etl_pipeline

2. Run the Docker Container with Persistency

docker run -d --name etl_pipeline \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  --env DB_NAME=RANDOMUSER \
  --env DB_USER=ANKITA123 \
  --env DB_PASSWORD=ANKITA \
  --env DB_HOST=localhost \
  --env DB_PORT=5432 \
  etl_pipeline

3. Verify Logs

Check the logs to ensure the ETL pipeline is running:

docker logs -f etl_pipeline

Productionization Steps

To deploy this ETL pipeline in a production environment, consider the following:

Use a Managed Database: Instead of a local PostgreSQL instance, use a managed service like AWS RDS, Google Cloud SQL, or Azure Database for PostgreSQL.

Environment Variables: Store database credentials securely using a secrets manager (e.g., AWS Secrets Manager, HashiCorp Vault) instead of hardcoding them.

Scalability: Deploy the containerized application using Kubernetes or Docker Swarm for horizontal scaling.

Monitoring & Logging: Use tools like Datadog, Prometheus, or ELK Stack to monitor application logs and performance metrics.

Automated Deployments: Implement CI/CD pipelines using GitHub Actions, Jenkins, or GitLab CI/CD for automated builds and deployments.

Cloud Storage: Store raw and processed data in cloud storage like AWS S3 or Google Cloud Storage for better durability and accessibility.

Error Handling & Alerts: Integrate alerting mechanisms to notify via email, Slack, or PagerDuty in case of failures.

Troubleshooting

Database Connection Issues: Ensure PostgreSQL is running and credentials are correct.

File Persistency Not Working: Make sure the correct volume paths are used while running the container.

Container Not Starting: Check logs using docker logs etl_pipeline.
