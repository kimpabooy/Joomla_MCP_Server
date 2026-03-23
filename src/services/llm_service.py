from openai import OpenAI
from openai.types.chat import ChatCompletionToolParam
from os import getenv
import json
from typing import Any, cast

"""
This module defines the available tools in a format compatible with OpenAI's function calling schema,
and provides a function to send user messages to the LLM and receive either a tool call or a text response.
More information: https://developers.openai.com/api/docs/guides/function-calling
"""

client = OpenAI(api_key=getenv("OPENAI_API_KEY"))

# OpenAI function-calling schema exposed to the model.
OPENAI_TOOL_SCHEMAS: list[ChatCompletionToolParam] = [
    {
        "type": "function",
        "function": {
            "name": "list_articles",
            "description": "Lista alla artiklar från Joomla",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_article",
            "description": "Hämta en specifik artikel baserat på ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "article_id": {"type": "integer", "description": "Artikelns ID"}
                },
                "required": ["article_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "publish",
            "description": "Publicera en artikel baserat på ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "article_id": {"type": "integer", "description": "Artikelns ID"}
                },
                "required": ["article_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "unpublish",
            "description": "Avpublicera en artikel baserat på ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "article_id": {"type": "integer", "description": "Artikelns ID"}
                },
                "required": ["article_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "trash",
            "description": "Flytta en artikel baserat på ID till papperskorgen",
            "parameters": {
                "type": "object",
                "properties": {
                    "article_id": {"type": "integer", "description": "Artikelns ID"}
                },
                "required": ["article_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_article",
            "description": "Skapa en ny artikel med titel och innehåll",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Artikelns titel"},
                    "content": {"type": "string", "description": "Artikelns innehåll/text"}
                },
                "required": ["title", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "edit_article",
            "description": "Redigera en befintlig artikel baserat på ID med nytt titel och innehåll",
            "parameters": {
                "type": "object",
                "properties": {
                    "article_id": {"type": "integer", "description": "Artikelns ID"},
                    "title": {"type": "string", "description": "Ny titel"},
                    "content": {"type": "string", "description": "Nytt innehåll"}
                },
                "required": ["article_id", "title", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_article",
            "description": "Ta bort en artikel permanent baserat på ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "article_id": {"type": "integer", "description": "Artikelns ID"}
                },
                "required": ["article_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "copy_article",
            "description": "Kopiera en befintlig artikel för att skapa en ny med en ny titel och samma innehåll",
            "parameters": {
                "type": "object",
                "properties": {
                    "article_id": {"type": "integer", "description": "Artikelns ID"},
                    "new_title": {"type": "string", "description": "Ny titel för den kopierade artikeln"}
                },
                "required": ["article_id", "new_title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_users",
            "description": "Hämta alla användare från Joomla",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_user",
            "description": "Hämta detaljer för en specifik användare baserat på deras ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "integer", "description": "Användarens ID"}
                },
                "required": ["user_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_user",
            "description": "Skapa en ny användare i Joomla med de givna detaljerna",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Användarens namn"},
                    "username": {"type": "string", "description": "Användarens användarnamn"},
                    "email": {"type": "string", "description": "Användarens e-postadress"},
                    "password": {"type": "string", "description": "Användarens lösenord"}
                },
                "required": ["name", "username", "email", "password"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_user",
            "description": "Ta bort en användare från Joomla baserat på deras ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "integer", "description": "Användarens ID"}
                },
                "required": ["user_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "edit_user",
            "description": "Redigera en befintlig användare i Joomla baserat på deras ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "integer", "description": "Användarens ID"},
                    "name": {"type": "string", "description": "Nytt namn"},
                    "username": {"type": "string", "description": "Nytt användarnamn"},
                    "email": {"type": "string", "description": "Ny e-postadress"}
                },
                "required": ["user_id", "name", "username", "email"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_unpublished_articles",
            "description": "Hämta alla opublicerade artiklar från Joomla",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },


    {
        "type": "function",
        "function": {
            "name": "get_menus",
            "description": "Hämta alla menyer från Joomla",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_menu",
            "description": "Hämta detaljer för en specifik meny baserat på dess ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "menu_id": {"type": "integer", "description": "Menyns ID"}
                },
                "required": ["menu_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_menu",
            "description": "Skapa en ny meny i Joomla med den givna titeln",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Menyns titel"}
                },
                "required": ["title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "edit_menu",
            "description": "Redigera en befintlig meny i Joomla baserat på dess ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "menu_id": {"type": "integer", "description": "Menyns ID"},
                    "title": {"type": "string", "description": "Ny menytitel"}
                },
                "required": ["menu_id", "title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
                "name": "delete_menu",
                "description": "Ta bort en meny från Joomla baserat på dess ID",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "menu_id": {"type": "integer", "description": "Menyns ID"}
                    },
                    "required": ["menu_id"]
                }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_menu_items",
            "description": "Hämta alla menyalternativ för en specifik meny baserat på dess ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "menu_id": {"type": "integer", "description": "Menyns ID"}
                },
                "required": ["menu_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_menu_item",
            "description": "Hämta detaljer för ett specifikt menyalternativ baserat på dess ID och den meny det tillhör",
            "parameters": {
                "type": "object",
                "properties": {
                    "menu_id": {"type": "integer", "description": "Menyns ID"},
                    "item_id": {"type": "integer", "description": "Menyalternativets ID"}
                },
                "required": ["menu_id", "item_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_menu_item",
            "description": "Skapa ett nytt menyalternativ under en specifik meny i Joomla",
            "parameters": {
                "type": "object",
                "properties": {
                    "menu_id": {"type": "integer", "description": "Menyns ID"},
                    "title": {"type": "string", "description": "Menyalternativets titel"},
                    "alias": {"type": "string", "description": "Menyalternativets alias"},
                    "link": {"type": "string", "description": "URL-länken för menyalternativet"}
                },
                "required": ["menu_id", "title", "alias", "link"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "edit_menu_item",
            "description": "Redigera ett befintligt menyalternativ i Joomla baserat på dess ID och den meny det tillhör",
            "parameters": {
                "type": "object",
                "properties": {
                    "menu_id": {"type": "integer", "description": "Menyns ID"},
                    "item_id": {"type": "integer", "description": "Menyalternativets ID"},
                    "title": {"type": "string", "description": "Ny titel för menyalternativet"},
                    "alias": {"type": "string", "description": "Nytt alias för menyalternativet"},
                    "link": {"type": "string", "description": "Ny URL-länk för menyalternativet"}
                },
                "required": ["menu_id", "item_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_menu_item",
            "description": "Ta bort ett menyalternativ från Joomla baserat på dess ID och den meny det tillhör",
            "parameters": {
                "type": "object",
                "properties": {
                    "menu_id": {"type": "integer", "description": "Menyns ID"},
                    "item_id": {"type": "integer", "description": "Menyalternativets ID"}
                },
                "required": ["menu_id", "item_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_tags",
            "description": "Hämta alla taggar från Joomla",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_tag",
            "description": "Hämta detaljer för en specifik tagg baserat på dess ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "tag_id": {"type": "integer", "description": "Taggens ID"}
                },
                "required": ["tag_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_tag",
            "description": "Skapa en ny tagg i Joomla med den givna titeln",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Taggens titel"}
                },
                "required": ["title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "edit_tag",
            "description": "Redigera en befintlig tagg i Joomla baserat på dess ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "tag_id": {"type": "integer", "description": "Taggens ID"},
                    "title": {"type": "string", "description": "Ny titel för taggen"}
                },
                "required": ["tag_id", "title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_tag",
            "description": "Ta bort en tagg från Joomla baserat på dess ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "tag_id": {"type": "integer", "description": "Taggens ID"}
                },
                "required": ["tag_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_tag_items",
            "description": "Hämta alla artiklar som är taggade med en specifik tagg baserat på taggens ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "tag_id": {"type": "integer", "description": "Taggens ID"}
                },
                "required": ["tag_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_tag_item",
            "description": "Hämta detaljer för en specifik artikel som är taggad med en specifik tagg baserat på både taggens ID och artikelns ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "tag_id": {"type": "integer", "description": "Taggens ID"},
                    "item_id": {"type": "integer", "description": "Artiklens ID"}
                },
                "required": ["tag_id", "item_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_tag_item",
            "description": "Tagga en artikel med en specifik tagg baserat på både taggens ID och artikelns ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "tag_id": {"type": "integer", "description": "Taggens ID"},
                    "item_id": {"type": "integer", "description": "Artiklens ID"}
                },
                "required": ["tag_id", "item_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "edit_tag_item",
            "description": "Redigera en taggning av en artikel med en specifik tagg baserat på både taggens ID och artikelns ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "tag_id": {"type": "integer", "description": "Taggens ID"},
                    "item_id": {"type": "integer", "description": "Artiklens ID"}
                },
                "required": ["tag_id", "item_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_tag_item",
            "description": "Ta bort en taggning av en artikel med en specifik tagg baserat på både taggens ID och artikelns ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "tag_id": {"type": "integer", "description": "Taggens ID"},
                    "item_id": {"type": "integer", "description": "Artiklens ID"}
                },
                "required": ["tag_id", "item_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_redirects",
            "description": "Hämta alla omdirigeringar från Joomla",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_redirect",
            "description": "Hämta detaljer för en specifik omdirigering baserat på dess ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "redirect_id": {"type": "integer", "description": "Omdirigeringens ID"}
                },
                "required": ["redirect_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_redirect",
            "description": "Skapa en ny omdirigering i Joomla",
            "parameters": {
                "type": "object",
                "properties": {
                    "source": {"type": "string", "description": "Källadressen för omdirigeringen"},
                    "destination": {"type": "string", "description": "Måladressen för omdirigeringen"}
                },
                "required": ["source", "destination"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "edit_redirect",
            "description": "Redigera en befintlig omdirigering i Joomla baserat på dess ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "redirect_id": {"type": "integer", "description": "Omdirigeringens ID"},
                    "source": {"type": "string", "description": "Källadressen för omdirigeringen"},
                    "destination": {"type": "string", "description": "Måladressen för omdirigeringen"}
                },
                "required": ["redirect_id", "source", "destination"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_redirect",
            "description": "Ta bort en omdirigering från Joomla baserat på dess ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "redirect_id": {"type": "integer", "description": "Omdirigeringens ID"}
                },
                "required": ["redirect_id"]
            }
        }
    },

]


def _parse_tool_args(raw_arguments: str | None) -> dict:
    """Parses the raw JSON string of tool arguments into a dictionary."""
    if not raw_arguments:
        return {}

    try:
        parsed = json.loads(raw_arguments)
        return parsed if isinstance(parsed, dict) else {}
    except json.JSONDecodeError:
        return {}


def ask_llm(messages: list[dict[str, Any]]) -> dict:
    """Sends a list of messages to the LLM and returns either tool calls or a text response."""
    response = client.chat.completions.create(
        max_tokens=500,
        model="gpt-4o-mini",
        messages=cast(Any, messages),
        tools=OPENAI_TOOL_SCHEMAS,
        tool_choice="auto"
    )

    message = response.choices[0].message

    if message.tool_calls:
        tool_calls = []
        assistant_tool_calls = []

        # If the LLM has decided to call tools, extract the tool calls and their arguments to return them in a structured format.
        for tool_call in message.tool_calls:
            toolfunction = getattr(tool_call, "function", None)
            if not toolfunction:
                continue

            # The raw arguments are a JSON string, parse them into a dictionary before returning.
            raw_arguments = toolfunction.arguments or "{}"
            tool_calls.append({
                "tool": toolfunction.name,
                "args": _parse_tool_args(raw_arguments),
                "tool_call_id": tool_call.id,
            })
            assistant_tool_calls.append({
                "id": tool_call.id,
                "type": "function",
                "function": {
                    "name": toolfunction.name,
                    "arguments": raw_arguments,
                },
            })

        if tool_calls:
            return {
                "tool_calls": tool_calls,
                "assistant_message": {
                    "role": "assistant",
                    "content": message.content or "",
                    "tool_calls": assistant_tool_calls,
                },
            }

    return {"text": message.content or ""}
