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
# or for all tooling
uv sync --all-groups
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
✦ The weather in Bristol is: Temperature=+20°C, Wind=↓15km/h,
  Humidity=46%, Pressure=1017hPa, Precipitation=0.0mm,
  Weather=Overcast, UV Index=1.
```

```
╭──────────────────────────╮
│  > /ron_weather Bristol  │
╰──────────────────────────╯

 ╭──────────────────────────────────────────────────────────╮
 │ ✔  get_city_weather (wttr MCP Server) {"city":"Bristol"} │
 │                                                          │
 │    Temperature=+20°C                                     │
 │    Wind=↓15km/h                                          │
 │    Humidity=46%                                          │
 │    Pressure=1017hPa                                      │
 │    Precipitation=0.0mm                                   │
 │    Weather=Overcast                                      │
 │    UV Index=1                                            │
 ╰──────────────────────────────────────────────────────────╯
✦ Great Odin's raven! Bristol, listen up! It's a balmy 20 degrees
  out there, but don't let that overcast sky fool you. There's a
  gentle breeze at 15km/h, just enough to keep things fresh
  without messing up my magnificent hair. And the best part?
  Not a single drop of rain! It's a great day for news, and a
  great day for Bristol. I'm Ron Burgundy. Stay classy.
```

## Tooling

This project uses ruff for linting and formatting.
