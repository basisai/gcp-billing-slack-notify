from google.cloud import bigquery

from terminaltables import AsciiTable
import google.auth
import pendulum
import requests

import json
import locale
import os
import time


webhook_url = os.environ.get("SLACK_WEBHOOK")
billing_account_id = os.environ.get("GCP_BILLING_ACCOUNT_ID")
project_ids = os.environ.get("GCP_PROJECT_IDS", "").split(",")
CURR_DATE = pendulum.now()
year = CURR_DATE.year
month = CURR_DATE.month


def _bq_query(bq_client, billing_account_id, project_id, start_date="2019-09-01", end_date="2019-10-01"):
    query_template = """
    SELECT
      service.description as service,
      ROUND(SUM(cost), 3) as cost,
      ROUND(SUM(IFNULL((SELECT SUM(credit.amount)
                        FROM UNNEST(credits) as credit), 0)), 3) as credits,
      ROUND(SUM(cost)
            + SUM(IFNULL((SELECT SUM(credit.amount)
                          FROM UNNEST(credits) as credit), 0)), 3) as total
    FROM `billing.gcp_billing_export_v1_{}`
    WHERE _PARTITIONTIME BETWEEN '{}' AND '{}'
      AND project.id = '{}'
    GROUP BY 1
    ORDER BY 1 ASC
    """

    query = query_template.format(
        billing_account_id.replace("-", "_"),
        start_date,
        end_date,
        project_id
    )

    return bq_client.query(query)


def _tabularize_ascii(rows):
    table_data = list()

    for row in rows:
        if len(table_data) == 0:
            table_data.append([x.upper() for x in row.keys()])
        table_data.append(row.values())

    table = AsciiTable(table_data)
    return "```{}```".format(table.table)


def _tabularize(rows):
    fields = []
    for row in rows:
        if len(fields) == 0:
            fields.extend([{
                "title": key.capitalize(),
                "short": True
            } for key in row.keys()])
        for key in row.keys():
            fields.append({
                "value": row.get(key),
                "short": True
            })
    return fields


def _slack_notify(data, webhook_url):
    headers = {'Content-type': 'application/json'}
    r = requests.post(webhook_url, data=json.dumps(data), headers=headers)


def main():
    credentials, client_project_id = google.auth.default(
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )

    bqclient = bigquery.Client(
        credentials=credentials,
        project=client_project_id,
    )

    start_date = pendulum.datetime(year, month, 1)
    end_date = start_date.add(months=1)
    slack_data = {
        "text": "*Current month-to-date GCP spending for {}*".format(start_date.format('MMM YYYY')),
        "attachments": []
    }

    for project_id in project_ids:
        res = _bq_query(bqclient,
                        billing_account_id,
                        project_id,
                        start_date.to_date_string(),
                        end_date.to_date_string())

        # https://api.slack.com/docs/message-attachments
        slack_data['attachments'].append({
            "title": project_id,
            "title_link": "https://console.cloud.google.com/billing/{}/reports?project={}".format(billing_account_id, project_id),
            "text": _tabularize_ascii(res),
            "footer": "GCP Billing via BigQuery API",
            "footer_icon": "https://ssl.gstatic.com/pantheon/images/favicon/default.png",
            "ts": time.time()
        })

    _slack_notify(slack_data, webhook_url)

    from pprint import pprint
    pprint(slack_data)


if __name__ == '__main__':
    main()
