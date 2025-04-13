ADHD Productivity Assistant: Condensed Plan
Overview
We’ll build a backend using Quart and LangChain. The system features:

Overseer Agent (GPT-4) that receives user messages and delegates tasks to tools.

Tools for:

Scheduling & Task Management (with persistent storage & check-ins).

Long-Term Memory (simple file-based JSON store).

Web Search (Tavily).

(Future) Microsoft Graph & Voice.

Persistent Scheduler to trigger reminders/check-ins across sessions.

Flow Outline
User Input via POST to /assistant/message.

Overseer Agent (GPT-4 w/ conversation memory) processes the request:

Decides if it can respond directly or needs to call a tool.

Tool Calls (via LangChain’s action→observation loop):

schedule_goal: break tasks into steps & schedule them (APScheduler / JSON store).

mark_task_done: mark steps complete.

store_memory / get_memory: file-based key-value store.

web_search: Tavily API to find real-time info.

Scheduler (BackgroundScheduler or similar) triggers check-ins at specified times.

Response: The overseer agent assembles a final reply for the user.

Core Components
Quart App:

Routes: /assistant/message, optional /tasks or /memory.

Calls agent with user text, returns the agent’s response.

LangChain Overseer Agent:

GPT-4 model, zero-shot or function-calling approach.

Tools array includes scheduling, memory, search.

Short-term conversation memory with ConversationBufferMemory.

Task Manager:

tasks.json storing goals & steps.

schedule_goal: parse durations/dates, create steps, schedule reminders.

mark_task_done: update status & persist.

Long-Term Memory:

memory.json storing key-value “memories”.

store_memory(item), get_memory(key).

Web Search:

web_search(query): Tavily integration returning text.

Scheduler:

APScheduler (or similar) with persistent job store to handle check-ins.

On startup, load tasks from tasks.json and schedule missed or upcoming jobs.

Future Enhancements
Microsoft Graph Tools: Outlook mail, contacts, calendar.

Voice Interface: STT input → agent → TTS output.

ChromaDB or other vector store for advanced memory & knowledge retrieval.