# GCP Billing Slack Notify

This repository contains the Docker image for running a Python script that notifies via Slack of your GCP spending.

This repository also contains a Helm chart to deploy this as a cron job on a Kubernetes cluster.

### Requirements

- Export billing data to BigQuery: https://cloud.google.com/billing/docs/how-to/export-data-bigquery
- Slack Incoming Webhook: https://api.slack.com/incoming-webhooks

### Docker Image

The Docker image is built and published to
[`quay/basisai/gcp-billing-slack-notify`](https://quay.io/basisai/gcp-billing-slack-notify).

### Environment variables configuration

| Env var | Description |
|---------|-------------|
| GOOGLE_APPLICATION_CREDENTIALS | Path to service account JSON keyfile |
| GCP_BILLING_ACCOUNT_ID | GCP billing account ID |
| GCP_PROJECT_IDS | Comma-seperated list of GCP project IDs |
| SLACK_WEBHOOK | Slack webhook URL |
