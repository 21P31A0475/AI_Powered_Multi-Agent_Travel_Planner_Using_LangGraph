import os
from typing import TypedDict, Annotated
import operator

import psycopg
from psycopg.rows import dict_row
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.postgres import PostgresSaver
from langchain_core.messages import (AnyMessage,HumanMessage,AIMessage,SystemMessage)

from langchain_groq import ChatGroq

from tools.tavily_tool import tavily_search
from tools.flight_tool import search_flights
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# LLM
llm = ChatGroq(
    model="openai/gpt-oss-120b"
)

# State
class TravelState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    user_query: str
    intent: str
    flight_results: str
    hotel_results: str
    itinerary: str
    llm_calls: int
    final_response: str


# Intent Router
def intent_router(state: TravelState):

    query = state["user_query"]

    response = llm.invoke([
        SystemMessage(content="""
You are a friendly conversational assistant for an AI Travel Planner.

Classify the user's message carefully.

CASE 1: GREETING OR CASUAL CHAT
Examples: hi, hii, hello, hey, good morning, how are you.
Respond with a natural, friendly greeting.
Do not mention Singapore, Tokyo, or any destination unless the user asks.

CASE 2: GENERAL QUESTIONS
Answer the user's question briefly and naturally.
Do not start travel agents.

CASE 3: ACTUAL TRAVEL REQUEST
Examples: plan a trip, find flights, search hotels,
create an itinerary, plan a holiday.
Return exactly:
TRAVEL

IMPORTANT:
Only return TRAVEL when the user clearly requests travel planning
or travel-related information.
For greetings and general questions, respond naturally.
"""),
        HumanMessage(content=query)
    ])

    answer = response.content.strip()

    if answer.strip().upper() == "TRAVEL":
        return {
            "intent": "travel",
            "llm_calls": state.get("llm_calls", 0) + 1
        }

    return {
        "intent": "chat",
        "final_response": answer,
        "messages": [AIMessage(content=answer)],
        "llm_calls": state.get("llm_calls", 0) + 1
    }


def route_after_intent(state: TravelState):

    if state["intent"] == "travel":
        return "flight_agent"

    return END

# Flight Agent
def flight_agent(state: TravelState):
    query = state["user_query"]
    flight_data = search_flights(query)
    return {
        "flight_results": flight_data,
        "messages": [
            AIMessage(content=f"Flight results fetched")
        ],
        "llm_calls": state.get("llm_calls", 0) + 1
    }

# Hotel Agent
def hotel_agent(state: TravelState):
    query = f"Best hotels for {state['user_query']}"
    hotel_results = tavily_search(query)

    return {
        "hotel_results": hotel_results,
        "messages": [
            AIMessage(content="Hotel information fetched")
        ],
        "llm_calls": state.get("llm_calls", 0) + 1
    }

# Itinerary Agent
def itinerary_agent(state: TravelState):

    prompt = f"""
    Create a travel itinerary.
    User Query:
    {state['user_query']}

    Flight Results:
    {state['flight_results']}

    Hotel Results:
    {state['hotel_results']}
    """

    response = llm.invoke([
        SystemMessage(
            content="You are an expert travel planner"
        ),
        HumanMessage(content=prompt)
    ])

    return {
        "itinerary": response.content,
        "messages": [response],
        "llm_calls": state.get("llm_calls", 0) + 1
    }

# Final Response Agent
def final_agent(state: TravelState):
    final_prompt = f"""
    Create the final travel response based on the user's actual request.

    User Query:
    {state['user_query']}

    Flights:
    {state['flight_results']}

    Hotels:
    {state['hotel_results']}

    Itinerary:
    {state['itinerary']}

    Do not introduce destinations that are not requested by the user.
    Do not invent flight availability or hotel bookings.
    """

    response = llm.invoke([
        SystemMessage(content="You are an expert travel planner."),
        HumanMessage(content=final_prompt)
    ])

    return {
        "messages": [response],
        "llm_calls": state.get("llm_calls", 0) + 1
    }

graph = StateGraph(TravelState)

graph.add_node("flight_agent", flight_agent)
graph.add_node("hotel_agent", hotel_agent)
graph.add_node("itinerary_agent", itinerary_agent)
graph.add_node("final_agent", final_agent)
graph.add_node("intent_router", intent_router)

graph.add_edge(START, "intent_router")
graph.add_conditional_edges(
    "intent_router",
    route_after_intent,
    {
        "flight_agent": "flight_agent",
        END: END
    }
)
graph.add_edge("flight_agent", "hotel_agent")
graph.add_edge("hotel_agent", "itinerary_agent")
graph.add_edge("itinerary_agent", "final_agent")
graph.add_edge("final_agent", END)


# Persistent connection so both CLI and Streamlit can share the compiled app
_conn = psycopg.connect(
    DATABASE_URL,
    autocommit=True,
    row_factory=dict_row
)

checkpointer = PostgresSaver(_conn)
checkpointer.setup()

app = graph.compile(checkpointer=checkpointer)


if __name__ == "__main__":
    config = {
        "configurable": {
            "thread_id": "user_chaitu"
        }
    }

    user_input = input("Enter travel request: ")

    result = app.invoke(
        {
            "messages": [
                HumanMessage(content=user_input)
            ],
            "user_query": user_input,
            "intent": "",
            "flight_results": "",
            "hotel_results": "",
            "itinerary": "",
            "llm_calls": 0,
            "final_response": ""
        },
        config=config
    )

    print("\nFINAL RESPONSE:\n")

    for msg in result["messages"]:
        print(msg.content)
