# mcp-wttr

A simple mcp server for returning weather data from wttr.in.

Made by following [this guide](https://modelcontextprotocol.io/quickstart/server).

The original implementation from the guide is [weather.py](./weather.py).

The wttr implementation is [wttr.py](./wttr.py).

## Installing

```bash
uv venv
source .venv/bin/activate
uv sync
```

### Add MCP Server - Gemini

```bash
mkdir -p ~/.gemini/extensions/wttr-extension
cat << EOF > ~/.gemini/extensions/wttr-extension/gemini-extension.json
{
  "name": "mcp-wttr",
  "version": "1.0.0",
  "mcpServers": {
    "wttr": {
      "command": "uv",
      "args": [
        "--directory",
        "$(pwd)",
        "run",
        "wttr.py"
      ]
    }
  }
}
EOF
```

## Debugging

Run the mcp inspector with
```bash
uv run mcp dev wttr.py
```

## Example - Gemini

```
> Get weather in Bristol

 ╭───────────────────────────────────────────────────────────╮
 │ ✔  get_city_weather (wttr MCP Server) {"city":"Bristol"}  │
 │                                                           │
 │    Temperature=+20°C                                      │
 │    Wind=↓15km/h                                           │
 │    Humidity=46%                                           │
 │    Pressure=1017hPa                                       │
 │    Precipitation=0.0mm                                    │
 │    Weather=Overcast                                       │
 │    UV Index=1                                             │
 ╰───────────────────────────────────────────────────────────╯
✦ The weather in Bristol is: Temperature=+20°C, Wind=↓15km/h, Humidity=46%, Pressure=1017hPa, Precipitation=0.0mm, Weather=Overcast, UV Index=1.
```
