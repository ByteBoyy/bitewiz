from __future__ import annotations
import json
from typing import Dict, List
from lib_llm.helpers.llm import LLM
from lib_llm.helpers.relevance_filter import RelevanceFilter
from lib_llm.helpers.tools import *
import asyncio
from lib_infrastructure.dispatcher import (Dispatcher, MessageType, Message, MessageHeader)


tools = [
    {
        "type": "function",
        "function": {
            "name": "search_restaurants",
            "description": "Search for restaurants that match specific moods, preferences or cuisines",
            "parameters": {
                "type": "object",
                "properties": {
                    "mood": {
                        "type": "string",
                        "description": "The mood/atmosphere the user is looking for (e.g., comforting, spicy, light, romantic)"
                    },
                    "preference": {
                        "type": "string",
                        "description": "Specific food preference or dish type the user wants (e.g., pasta, burger, vegetarian)"
                    },
                    "cuisine": {
                        "type": "string",
                        "description": "Specific cuisine type (e.g., Italian, Japanese, Mexican)"
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_restaurant_menu",
            "description": "Get the menu for a specific restaurant with flavor profiles highlighted",
            "parameters": {
                "type": "object",
                "properties": {
                    "restaurant_name": {
                        "type": "string",
                        "description": "The Name for Resturant (e.g., olive resturant, curry palace)"
                    }
                },
                "required": ["restaurant_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "save_order",
            "description": "Save the user's order details to a JSON file",
            "parameters": {
                "type": "object",
                "properties": {
                    "restaurant_name": {
                        "type": "string",
                        "description": "The name of the restaurant the user is ordering from"
                    },
                    "items": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {
                                    "type": "string",
                                    "description": "Name of the food item"
                                },
                                "quantity": {
                                    "type": "integer",
                                    "description": "How many of this item the user wants to order"
                                },
                                "price": {
                                    "type": "number",
                                    "description": "Price of a single item"
                                },
                                "description": {
                                    "type": "string",
                                    "description": "Optional description of the item"
                                }
                            },
                            "required": ["name", "quantity", "price"]
                        },
                        "description": "Array of items the user wants to order"
                    }
                },
                "required": ["restaurant_name", "items"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_cuisines",
            "description": "Search for restaurants that match user's specific cuisines",
            "parameters": {
                "type": "object",
                "properties": {
                    "cuisine": {
                        "type": "string",
                        "description": "Specific cuisine type (e.g., Italian, Japanese, Mexican)"
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_dietary_preferences",
            "description": "Search for all available dietary preferences",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]



tool_implementations = {
    "search_restaurants": search_restaurants,
    "get_restaurant_menu": get_restaurant_menu,
    "search_cuisines": search_cuisines,
    "save_order": save_order,
    "get_dietary_preferences" : get_dietary_preferences
}

class LargeLanguageModel:
    def __init__(self, guid , lat : float , long : float, llm: LLM, dispatcher: Dispatcher,source: str = "device"):
        self.guid = guid
        self.llm = llm
        self.dispatcher = dispatcher
        llm.tools = tools
        self.lat = lat
        self.long = long
        self.source = source
        self.is_audio_required = True
        self.relevance_filter = RelevanceFilter()
        self.recent_messages = []
        self.max_context_messages = 5



    async def process(self, message: LLM.LLMMessage):
        if message.role == LLM.Role.USER:
            is_relevant = self.relevance_filter.is_relevant_with_context(
                message.content, 
                self.recent_messages,
                threshold=0.55
            )
            
            if not is_relevant:
                print(f"🔇 Filtering out: '{message.content}'")
                return
            
            self.recent_messages.append(message.content)
            if len(self.recent_messages) > self.max_context_messages:
                self.recent_messages.pop(0)

        llm_words = []
        async for words in self.llm.create_completion(message=message):
            if isinstance(words, Dict):
                # Send Clear Buffer Event
                await self.dispatcher.broadcast(
                    self.guid,
                    Message(
                        MessageHeader(MessageType.CLEAR_EXISTING_BUFFER),
                        data = {},
                    )
                )

                print(f"[TOOL_CALL] : {words}")

                func = tool_implementations.get( words.get('name') )
                tool_call_id = words.get('id')
                if func : 
                    func_args = words.get('args' , {})
                    # Add lat and long to the function arguments if they are not already present
                    func_args['lat'] = self.lat
                    func_args['long'] = self.long
                    func_args['source'] = self.source
                    result = func(func_args)
                    if result.get('is_llm_needed') : 
                        await self.dispatcher.broadcast(
                                self.guid,
                                Message(
                                    MessageHeader(MessageType.FINAL_TRANSCRIPTION_CREATED),
                                    data=LLM.LLMMessage(
                                        role=LLM.Role.SYSTEM,
                                        content=json.dumps(result.get("data")),
                                    ),
                                ),
                            )
                    else : 
                        llm_words = result.get('data')
                        strucutred_data = result.get('api_data', {})
                        api_data_type = result.get('type' , None)

                        # Append the structured data to the function responses
                        await self.dispatcher.broadcast(
                                self.guid,
                                Message(
                                    MessageHeader(MessageType.STRUCTURED_DATA),
                                    data={"id": tool_call_id, "api_data": strucutred_data , "type": api_data_type},
                                ),
                            )

                        # First add the assistant's message with tool calls
                        self.llm.messages.append({
                            "role": LLM.Role.ASSISTANT.value,
                            "tool_calls": [
                                { "id":tool_call_id , "type": "function", 
                                "function": { "name":  words.get('name') , "arguments": json.dumps(func_args) } }
                            ]
                        })

                        message = LLM.LLMMessage(role=LLM.Role.TOOL, content=json.dumps(llm_words) , tool_call_id = words.get('id'))
                        await self.process(message=message)
                    

            else : 
                words = words.lower()
                llm_words.append(words)

                await self.dispatcher.broadcast(
                    self.guid,
                    Message(
                        MessageHeader(
                            MessageType.LLM_GENERATED_TEXT
                        ),
                        data={"words" : words ,"is_audio_required" : self.is_audio_required},
                    ),
                )

        words = "".join(llm_words)
        await self.dispatcher.broadcast(
        self.guid,
        Message(
            MessageHeader(
                MessageType.TTS_FLUSH
            ),
            data=words,
        ),
        )
 
    async def run_async(self):
        async with await self.dispatcher.subscribe(
            self.guid, MessageType.CALL_ENDED
        ) as call_ended_subscriber, await self.dispatcher.subscribe(
            self.guid, MessageType.FINAL_TRANSCRIPTION_CREATED
        ) as transcription_created_subscriber:
            
            async for event in transcription_created_subscriber:
                if "CLICK_EVENT" in event.message.data.content :  self.is_audio_required = False
                else : self.is_audio_required = True
                await self.process(message=event.message.data)

                call_ended_message = await self.dispatcher.get_nowait(
                    call_ended_subscriber
                )
                if call_ended_message is not None:
                    break

