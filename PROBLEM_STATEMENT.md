# MarketMate - Chatbot Application Assignment

## Objective
Build a chatbot application named **MarketMate** that allows users to interact with various large language models (LLMs). The application should provide basic functionalities for interacting with these models while maintaining certain constraints and rate limits. Additionally, the chatbot is tailored specifically for answering questions related to **financial market data**.

---

## Requirements

### Chat Interface
1. Users should be able to send and receive messages in a conversational flow.
2. Conversations should preserve context (previous messages) within a session.
3. Users should be able to start a new chat session, resetting the context.
4. Users should be able to see past conversations and continue any conversation by simply sending a message in the chat window.

---

### System Message
1. Each conversation should begin with a **system message** that directs the LLM on how to assist the user for the given use case.
2. The conversation flow should follow this pattern:  
   `[System Message] → [User Message] → [AI Response] → [User Message] → [AI Response] → ...`
3. When a user starts a new conversation, the **first message** sent to the LLM should be a system message providing instructions to the LLM on how to assist the user and other guidelines. The user message follows.

---

### LLM Provider
1. Use an **LLM Provider API** to chat with any language model. The model should respond to the user message based on the instructions in the system message.
2. The LLM can be directed to make **function calls** when necessary. If the LLM responds with a function call, the system should execute the function call and return the response to the LLM, which can then use it to answer the original question.
3. Use the **request/response structures** provided in the reference section. Feel free to modify them as needed.

---

### Rate Limits
1. Implement **tiered rate limits** to manage application usage by users.
2. **Tiers:** Free, Tier-1, Tier-2, Tier-3.
3. **Rate limit measurement:**  
   - Requests per minute (RPM)  
   - Requests per day (RPD)  
   - Tokens per minute (TPM)  
   - Tokens per day (TPD)
4. The rate limits are defined for each **(Tier, Provider, Model)** tuple.
5. On reaching any rate limit, throw an **error message** that is user-friendly and provides actionable insights.
6. Example rate limits:

   | Tier     | Provider | Model  | RPM   | RPD    | TPM      | TPD        |
   |----------|----------|--------|-------|--------|----------|------------|
   | Free     | OpenAI   | gpt-4o | 3     | 200    | 40,000   | 1,000,000  |
   | Tier-1   | OpenAI   | gpt-4o | 500   | 10,000 | 200,000  | 5,000,000  |
   | Tier-2   | OpenAI   | gpt-4o | 5,000 | 100,000| 2,000,000| 50,000,000 |
   | Tier-3   | OpenAI   | gpt-4o | 50,000| 1,000,000| 20,000,000|500,000,000|

---

### Financial Market Data
1. The chatbot should **only handle queries related to financial market data**. Questions outside this context should not be answered.
2. Use available APIs to get financial market data for a given company to answer user questions accurately.
3. Use a **Financial News API** to get the latest financial news for a given company. This includes:
   - Important events (e.g., big investments, future initiatives, large collaborations).
4. Use a **Quarterly Financial Results API** to retrieve:
   - Balance sheets, P&L, cash flow, transcripts of analyst calls, valuation ratios, etc.  
     For example, use platforms like **screener.in** for companies listed in Indian stock exchanges.
5. Use the **request/response structures** provided in the reference section. Feel free to modify them as needed.

---

## Submission Details

### Expectations
- The implementation can focus on **frontend**, **backend**, or both, depending on your skills. **Play to your strengths.**
- Choose any **programming language** and **framework**.
- The design and implementation should reflect your **thought process**. Comments in the code are appreciated.
- We are evaluating how you handle **ambiguity** and your **bias toward action**.
- A **polished product** is not expected. Focus on **functionality** and **clarity of thought**.
- A **mock implementation** is acceptable since all APIs are placeholders. You may:
  - Replace dummy APIs with actual APIs (e.g., OpenAI, Gemini, etc.).
  - Create mock functions to simulate responses.
- **Time limit:** Do not spend more than **a day** on this assignment.
