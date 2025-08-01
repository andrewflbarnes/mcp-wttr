import httpx
import ssl
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("wttr")
ssl = ssl.create_default_context()
client = httpx.Client(verify=ssl)


async def get_weather(city: str) -> str:
    url = (f"http://wttr.in/{city}?format="
           "Temperature=%t\\n"
           "Wind=%w\\n"
           "Humidity=%h\\n"
           "Pressure=%P\\n"
           "Precipitation=%p\\n"
           "Weather=%C\\n"
           "UV%20Index=%u"
           )

    try:
        response = client.get(url)
        response.raise_for_status()
        return response.text.strip()
    except httpx.HTTPStatusError as e:
        return (f"Error fetching weather: {e.response.status_code}"
                f" - {e.response.text}"
                )
    except Exception as e:
        return f"An error occurred: {str(e)}"


@mcp.tool()
async def get_city_weather(city: str) -> str:
    """Get weather for a specific city.

    Args:
        city (str): The name of the city to get the weather for.
    """
    return await get_weather(city)


if __name__ == "__main__":
    mcp.run(transport="stdio")
