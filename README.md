# eon_elpris
Integration for Home Assistant that adds average electric price for current month as a sensor from E.on in Sweden.

This integration provides the monthly average electricity price used by E.ON Sweden.
On their site they show what the monthly price might become and it updates based on prices, taxes and usage of other consumers.
Hence it is pretty close to the final price per month.

Data (API) source:
https://eonepapirun.azurewebsites.net/api/getSpotpricesAverage

## Features

- Select price area (SE1, SE2, SE3, SE4)
- Choose unit (öre/kWh or kr/kWh)
- Hourly updates
- Attributes for month and validity period

## Installation

Install via HACS → Custom repository.

Then add the integration via:

Settings → Devices & Services → Add Integration → E.ON Monthly Electricity Price
