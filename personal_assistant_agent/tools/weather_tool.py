from __future__ import annotations

from typing import Any

import requests

from personal_assistant_agent.core.base_tool import BaseTool


class WeatherTool(BaseTool):
    @property
    def name(self) -> str:
        return "get_weather"

    @property
    def description(self) -> str:
        return "Fetches current weather information for a city."

    def get_declaration(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City name, e.g., 'Johannesburg' or 'London'.",
                    }
                },
                "required": ["city"],
            },
        }

    def execute(self, **kwargs: Any) -> dict[str, Any]:
        city = str(kwargs["city"]).strip()
        if not city:
            return {"ok": False, "error": "City must not be empty."}

        url = f"https://wttr.in/{city}"
        params = {"format": "j1"}

        try:
            response = requests.get(url, params=params, timeout=12)
            response.raise_for_status()
            payload = response.json()

            current = payload.get("current_condition", [{}])[0]
            nearest = payload.get("nearest_area", [{}])[0]
            area = nearest.get("areaName", [{}])[0].get("value", city)
            country = nearest.get("country", [{}])[0].get("value", "Unknown")

            return {
                "ok": True,
                "city": area,
                "country": country,
                "temperature_c": current.get("temp_C"),
                "feels_like_c": current.get("FeelsLikeC"),
                "humidity": current.get("humidity"),
                "description": (current.get("weatherDesc", [{}])[0].get("value", "Unknown")),
                "wind_kmph": current.get("windspeedKmph"),
            }
        except requests.RequestException as exc:
            return {
                "ok": False,
                "error": "Weather request failed.",
                "details": str(exc),
                "city": city,
            }
        except ValueError as exc:
            return {
                "ok": False,
                "error": "Weather service returned invalid JSON.",
                "details": str(exc),
                "city": city,
            }
