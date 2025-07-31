from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
import sys

mcp = FastMCP("weather")

NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"


async def get_weather_data(url: str) -> dict[str, Any] | None:
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None


def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    props = feature["properties"]
    return f"""
Event: {props.get('event', 'Unknown')}
Area: {props.get('areaDesc', 'Unknown')}
Severity: {props.get('severity', 'Unknown')}
Description: {props.get('description', 'No description available')}
Instructions: {props.get('instruction', 'No specific instructions provided')}
"""


@mcp.tool()
async def get_alerts(state: str) -> str:
    """
    Get weather alerts for a specific state.

    Args:
        state (str): The two-letter state abbreviation (e.g., 'CA' for California).

    Returns:
        str: A formatted string of weather alerts or a message if no alerts are found.
    """
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await get_weather_data(url)

    if not data or "features" not in data or not data["features"]:
        return "No active weather alerts found."

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n--\n".join(alerts)


@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """
    Get the weather forecast for a specific latitude and longitude.

    Args:
        latitude (float): Latitude of the location.
        longitude (float): Longitude of the location.

    Returns:
        str: A formatted string of the weather forecast or an error message.
    """
    url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    data = await get_weather_data(url)

    print(f"Received data: {data}", file=sys.stderr)

    if not data:
        return "No forecast data available."

    forecast_url = data.get("properties", {}).get("forecast")
    if not forecast_url:
        return "No forecast URL found in the response."

    forecast_data = await get_weather_data(forecast_url)
    print(f"Received forecast: {forecast_data}", file=sys.stderr)

    if not forecast_data or "properties" not in forecast_data:
        return "No forecast data available."

    periods = forecast_data["properties"].get("periods", [])
    if not periods:
        return "No forecast periods available."

    forecasts = []
    for period in periods[:5]:  # Only show next 5 periods
        forecast = f"""
{period['name']}:
Temperature: {period['temperature']}°{period['temperatureUnit']}
Wind: {period['windSpeed']} {period['windDirection']}
Forecast: {period['detailedForecast']}
"""
        forecasts.append(forecast)

    return "\n---\n".join(forecasts)

if __name__ == "__main__":
    mcp.run(transport="stdio")
