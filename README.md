# enecoQ Home Assistant Integration

This is a Home Assistant integration for reading enecoQ data from JSON files. It provides sensors for today's and this month's electricity usage, cost, and CO2 emissions.

## Installation

You can install this integration via HACS. Search for "enecoQ" in the HACS integrations section or use the following URL:

https://my.home-assistant.io/redirect/hacs_repository/?category=integration&owner=kishikawakatsumi&repository=enecoq-ha-integration

## Configuration

After installing the integration, you can configure it via the Home Assistant UI. You will need to provide the paths to the JSON files for today's and this month's data, as well as the number of minutes after which the data is considered stale.

## Sensors

The integration provides the following sensors:

- `sensor.enecoq_today_usage`: Today's electricity usage in kWh.
- `sensor.enecoq_today_cost`: Today's electricity cost in your currency.
- `sensor.enecoq_today_co2`: Today's CO2 emissions in kg.
- `sensor.enecoq_today_timestamp`: The timestamp of the latest data for today.
- `sensor.enecoq_month_usage`: This month's electricity usage in kWh.
- `sensor.enecoq_month_cost`: This month's electricity cost in your currency.
- `sensor.enecoq_month_co2`: This month's CO2 emissions in kg.
- `sensor.enecoq_month_timestamp`: The timestamp of the latest data for this month.
