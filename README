# ✈️ AI-Powered Multi-Agent Travel Planner Using Langgraph

An intelligent AI-powered travel planning assistant built using **LangGraph, Groq LLM, and PostgreSQL**. The system uses a multi-agent architecture to understand user requests, search for flights and hotels, and generate personalized travel itineraries.

## 🚀 Project Overview

The AI Travel Planner is a conversational assistant that helps users plan their trips efficiently.

It intelligently classifies user messages into different categories:

- **Greeting & Casual Chat:** Responds naturally to greetings and casual conversations.
- **General Questions:** Answers general questions without triggering travel agents.
- **Travel Requests:** Activates the multi-agent travel planning workflow.

For actual travel requests, multiple agents work together to collect travel information and generate a structured itinerary.

## ✨ Key Features

- **Intent Classification:** Identifies whether the user wants casual conversation, general information, or travel planning.
- **Flight Search Agent:** Searches for flight information based on the user's travel request.
- **Hotel Search Agent:** Finds relevant hotel information using Tavily search.
- **Itinerary Generation Agent:** Creates a travel itinerary using flight and hotel information.
- **Final Response Agent:** Combines all collected information into a user-friendly response.
- **Conversational AI:** Powered by Groq LLM.
- **Persistent Memory:** Uses PostgreSQL checkpointing to maintain conversation state across interactions.
- **Multi-Agent Workflow:** Uses LangGraph to coordinate different agents.

## 🏗️ System Architecture

The project follows a sequential multi-agent architecture.

```text
                 USER INPUT
                     |
                     v
              INTENT ROUTER
                     |
             +-------+-------+
             |               |
          GENERAL          TRAVEL
           CHAT           REQUEST
             |               |
             v               v
          RESPONSE      FLIGHT AGENT
                             |
                             v
                         HOTEL AGENT
                             |
                             v
                      ITINERARY AGENT
                             |
                             v
                       FINAL AGENT
                             |
                             v
                       FINAL OUTPUT
```

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| LangGraph | Multi-agent workflow orchestration |
| Groq LLM | Natural language understanding and generation |
| PostgreSQL | Persistent conversation checkpointing |
| Psycopg | PostgreSQL database connectivity |
| Tavily | Hotel information search |
| Flight Search Tool | Flight information retrieval |
| LangChain | Message handling and LLM integration |
| python-dotenv | Environment variable management |

## 📁 Project Structure

```text
AI-Travel-Planner/
│
├── tools/
│   ├── flight_tool.py
│   └── tavily_tool.py
│
├── app.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/AI-Travel-Planner.git
```

### 2. Navigate to the Project Directory

```bash
cd AI-Travel-Planner
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

**Windows:**

```bash
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file in the root directory.

```env
DATABASE_URL=your_postgresql_connection_string
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Add any additional API credentials required by your flight search tool.

### 6. Set Up PostgreSQL

Create a PostgreSQL database and configure the connection string in your `.env` file.

The application uses `PostgresSaver` to create and manage checkpoint tables.

### 7. Run the Application

```bash
python app.py
```

Enter your travel request when prompted.

## 💬 Example User Queries

**Greeting:**

```text
User: Hi!
Assistant: Hello! How can I help you today?
```

**Flight and Hotel Search:**

```text
User: Find flights and hotels for a trip from Hyderabad to Goa.
```

**Travel Itinerary:**

```text
User: Plan a 5-day trip to Singapore with flights and hotels.
```

**General Question:**

```text
User: What is the capital of Japan?
```

## 🔄 Workflow Explanation

1. **Intent Router:** Analyzes the user's query using Groq LLM and identifies the intent.
2. **Flight Agent:** Calls the flight search tool to retrieve flight information.
3. **Hotel Agent:** Uses Tavily to search for relevant hotel information.
4. **Itinerary Agent:** Generates a travel itinerary using the collected information.
5. **Final Response Agent:** Produces the final travel response based on the user's request and available search results.

## 💾 Database and Memory

PostgreSQL is integrated with LangGraph using `PostgresSaver`.

The checkpointer stores graph execution state and enables conversation continuity through thread IDs.

This allows the application to maintain conversation context across multiple interactions using the same thread.

## 🔮 Future Enhancements

- Personalized travel recommendations.
- Budget-based trip planning.
- Real-time flight and hotel availability integration.
- Weather-based travel suggestions.
- Multiple destination trip planning.
- User authentication and individual conversation histories.
- Travel booking API integration.
