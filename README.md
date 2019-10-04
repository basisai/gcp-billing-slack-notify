# gcp-billing-slack-notify

This repository contains the Docker image for running a Python script that notifies via Slack of your GCP spending.

This repository also contains a Helm chart to deploy this as a cron job on a Kubernetes cluster.

### Docker Image

The Docker image is built and published to
[`basisai/gcp-billing-slack-notify`](https://hub.docker.com/r/basisai/gcp-billing-slack-notify).

### Environment variables configuration

| Env var | Description |
|---------|-------------|
| GOOGLE_APPLICATION_CREDENTIALS | Path to service account JSON keyfile |
| GCP_BILLING_ACCOUNT_ID | GCP billing account ID |
| GCP_PROJECT_IDS | Comma-seperated list of GCP project IDs |
| SLACK_WEBHOOK | Slack webhook URL |
