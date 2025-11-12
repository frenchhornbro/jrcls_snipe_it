# jrcls-snipe-it

This script
- Records changes to consumables in a report and emails them once a week
- Sends an order request for each consumables below minimum quantity

## Installation

Install dependencies:

```
pip install -r requirements.txt
```

Create config file:

```
cp example-config.json config.json
```

Edit config file and replace `sender-email-app-password` with the actual app password and `api-token` with a generated API token from Snipe-IT.

## Stored files

comparison.json is the current state of the assets.

weekly-report.txt is a report of changes to consumables throughout the week, as well as orders placed.

log.txt contains a log of actions taken by the script.