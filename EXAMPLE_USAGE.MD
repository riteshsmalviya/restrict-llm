#  restrict-llm — Travel Itinerary Example

This example demonstrates using **restrict-llm** as a proxy to generate a structured travel itinerary from an LLM, with JSON validation enforced by the proxy.

---

##  Request

**Endpoint:** `POST /v1/restrictllm/generate`

```json
{
  "llm": {
    "url": "https://openrouter.ai/api/v1/chat/completions",
    "method": "POST",
    "headers": {
      "Authorization": "Bearer <YOUR_OPENROUTER_API_KEY>",
      "Content-Type": "application/json"
    },
    "bodyTemplate": {
      "model": "nvidia/nemotron-3-nano-30b-a3b:free",
      "messages": [
        {
          "role": "system",
          "content": "You are a travel planner. You MUST respond with ONLY a valid JSON object. No markdown, no explanation, no code fences. Just raw JSON."
        },
        {
          "role": "user",
          "content": "{{prompt}}"
        }
      ],
      "reasoning": { "enabled": true }
    },
    "responsePath": "choices.0.message.content"
  },
  "prompt": "Create a travel itinerary for Goa, India. Start date: 2025-03-01, End date: 2025-03-05, Number of people: 2, Budget: 30000 INR. Return ONLY this JSON structure with no extra text:\n{\n  \"destination\": \"\",\n  \"startDate\": \"\",\n  \"endDate\": \"\",\n  \"numberOfPeople\": \"\",\n  \"totalBudget\": 0,\n  \"summary\": \"\",\n  \"budgetBreakdown\": {\n    \"accommodation\": 0,\n    \"food\": 0,\n    \"activities\": 0,\n    \"transportation\": 0,\n    \"shopping\": 0,\n    \"miscellaneous\": 0\n  },\n  \"dayPlans\": [\n    {\n      \"dayNumber\": 1,\n      \"date\": \"\",\n      \"title\": \"\",\n      \"estimatedCost\": 0,\n      \"activities\": [\n        { \"time\": \"\", \"name\": \"\", \"description\": \"\", \"cost\": 0, \"category\": \"\" }\n      ]\n    }\n  ],\n  \"recommendations\": [\"\"]\n}",
  "rules": {
    "format": "json",
    "requiredKeys": ["destination", "dayPlans", "budgetBreakdown"],
    "retryAttempts": 3
  }
}
```

> **How `{{prompt}}` works:** The proxy replaces `{{prompt}}` in `bodyTemplate` with the value of the top-level `prompt` field before forwarding to the LLM.

> **How `rules` work:** The proxy validates the LLM response is valid JSON and contains the required keys. If not, it automatically retries up to 3 times.

---

##  Response

```json
{
  "result": {
    "destination": "Goa, India",
    "startDate": "2025-03-01",
    "endDate": "2025-03-05",
    "numberOfPeople": 2,
    "totalBudget": 30000,
    "summary": "A 5-day Goa beach getaway for two people covering accommodation, food, activities, transportation, shopping, and miscellaneous expenses within a ₹30,000 budget.",
    "budgetBreakdown": {
      "accommodation": 12000,
      "food": 8000,
      "activities": 5000,
      "transportation": 3000,
      "shopping": 1500,
      "miscellaneous": 500
    },
    "dayPlans": [
      {
        "dayNumber": 1,
        "date": "2025-03-01",
        "title": "Arrival and Beach Walk",
        "estimatedCost": 6000,
        "activities": [
          { "time": "09:00", "name": "Hotel Check-in",     "description": "Check into your beachfront hotel and freshen up",    "cost": 2400, "category": "accommodation"  },
          { "time": "12:30", "name": "Lunch at Beach Shack","description": "Fresh seafood lunch at a local beach shack",         "cost": 1600, "category": "food"           },
          { "time": "14:00", "name": "Surfing Lesson",      "description": "Beginner-friendly surfing session with instructor",   "cost": 1000, "category": "activities"     },
          { "time": "16:00", "name": "Airport Transfer",    "description": "Taxi ride from airport to hotel",                    "cost":  600, "category": "transportation" },
          { "time": "18:30", "name": "Souvenir Shopping",   "description": "Explore local shops and buy handicrafts",            "cost":  300, "category": "shopping"       },
          { "time": "20:30", "name": "Evening Cocktail",    "description": "Relax with a drink while watching the sunset",       "cost":  100, "category": "miscellaneous"  }
        ]
      },
      {
        "dayNumber": 2,
        "date": "2025-03-02",
        "title": "Cultural Exploration Day",
        "estimatedCost": 6000,
        "activities": [
          { "time": "09:00", "name": "Hotel Stay",          "description": "Morning relaxation at hotel",                       "cost": 2400, "category": "accommodation"  },
          { "time": "12:00", "name": "Traditional Goan Lunch","description": "Authentic Goan thali",                            "cost": 1600, "category": "food"           },
          { "time": "13:30", "name": "Historic Tour",       "description": "Visit Basilica of Bom Jesus and Se Cathedral",      "cost": 1000, "category": "activities"     },
          { "time": "15:30", "name": "Taxi Travel",         "description": "Travel between heritage locations",                 "cost":  600, "category": "transportation" },
          { "time": "17:30", "name": "Anjuna Market Visit", "description": "Shop for local goods and souvenirs",               "cost":  300, "category": "shopping"       },
          { "time": "19:30", "name": "Beach Walk",          "description": "Evening beach stroll",                             "cost":  100, "category": "miscellaneous"  }
        ]
      },
      {
        "dayNumber": 3,
        "date": "2025-03-03",
        "title": "Full Beach and Adventure Day",
        "estimatedCost": 6000,
        "activities": [
          { "time": "08:00", "name": "Hotel Stay",          "description": "Continue hotel stay",                              "cost": 2400, "category": "accommodation"  },
          { "time": "10:00", "name": "Beach Relaxation",    "description": "Relax at Calangute Beach",                        "cost": 1600, "category": "food"           },
          { "time": "12:30", "name": "Water Sports",        "description": "Jet skiing and parasailing",                      "cost": 1000, "category": "activities"     },
          { "time": "15:00", "name": "Local Transport",     "description": "Travel to nearby village",                        "cost":  600, "category": "transportation" },
          { "time": "17:00", "name": "Local Market Visit",  "description": "Buy spices, tea, and souvenirs",                  "cost":  300, "category": "shopping"       },
          { "time": "19:00", "name": "Beach Dinner",        "description": "BBQ dinner by the beach",                        "cost":  100, "category": "miscellaneous"  }
        ]
      },
      {
        "dayNumber": 4,
        "date": "2025-03-04",
        "title": "Adventure and Relaxation",
        "estimatedCost": 6000,
        "activities": [
          { "time": "09:00", "name": "Hotel Stay",          "description": "Enjoy your beachfront hotel",                     "cost": 2400, "category": "accommodation"  },
          { "time": "11:30", "name": "Breakfast",           "description": "Hotel buffet breakfast",                          "cost": 1600, "category": "food"           },
          { "time": "13:00", "name": "Dolphin Watching",    "description": "Boat tour from Palolem Beach",                    "cost": 1000, "category": "activities"     },
          { "time": "15:30", "name": "Taxi Transfer",       "description": "Travel to another beach location",               "cost":  600, "category": "transportation" },
          { "time": "17:00", "name": "Shopping",            "description": "Buy clothes and accessories",                    "cost":  300, "category": "shopping"       },
          { "time": "19:30", "name": "Night Drink",         "description": "Cocktail at beach bar",                          "cost":  100, "category": "miscellaneous"  }
        ]
      },
      {
        "dayNumber": 5,
        "date": "2025-03-05",
        "title": "Departure Day",
        "estimatedCost": 6000,
        "activities": [
          { "time": "08:00", "name": "Hotel Checkout",      "description": "Checkout and prepare for departure",              "cost": 2400, "category": "accommodation"  },
          { "time": "10:00", "name": "Brunch",              "description": "Final Goan brunch",                              "cost": 1600, "category": "food"           },
          { "time": "12:00", "name": "Spa Treatment",       "description": "Relaxing massage session",                       "cost": 1000, "category": "activities"     },
          { "time": "14:00", "name": "Airport Transfer",    "description": "Taxi ride to airport",                           "cost":  600, "category": "transportation" },
          { "time": "16:00", "name": "Last-minute Shopping","description": "Buy gifts and souvenirs",                        "cost":  300, "category": "shopping"       },
          { "time": "18:00", "name": "Farewell Drink",      "description": "Final relaxing drink before departure",          "cost":  100, "category": "miscellaneous"  }
        ]
      }
    ],
    "recommendations": [
      "Rent a scooter for affordable and flexible travel",
      "Try authentic Goan seafood such as fish thali",
      "Visit Old Goa churches and cultural heritage sites",
      "Watch sunset at Anjuna or Palolem Beach",
      "Stay hydrated and use sunscreen regularly"
    ]
  }
}
```

---

## Tips for Structured JSON Responses

1. **Add a `system` message instructing JSON-only output** — Prevents the model from adding explanatory text around the JSON.
2. **Embed the full JSON schema in the `prompt`** — The model knows exactly which fields to populate and in what shape.
3. **Set `rules.format: "json"`** — The proxy validates the response is parseable JSON before returning it.
4. **Set `rules.requiredKeys`** — The proxy retries automatically if any critical top-level fields are missing.
5. **Set `rules.retryAttempts: 3`** — Auto-retries if the model returns markdown fences or malformed JSON.
