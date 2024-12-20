# MarketMate 

## Quick Start Guide

1. **Clone Repo:**
   ```bash
   git clone <repository-url> && cd <repository-directory>
   ```

2. **Setup Virtual Env:**
   ```bash
   python3 -m venv venv && source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install Packages:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Environment Variables:**
   Create a `.env` file and add `OPENAI_API_KEY` and `MONGO_URI` keys.

5. **Activate MongoDB Instance:**
   - **Locally:** Ensure MongoDB is installed and running on your machine.
   - **Hosted Service:** Use a service like MongoDB Atlas and ensure your `MONGO_URI` is correctly configured.

6. **Run Backend:**
   ```bash
   python application.py
   ```

7. **Run Frontend:**
   ```bash
   streamlit run streamlit-app.py
   ```

8. **Open App:**
   Visit `http://localhost:8501` in your browser.

9. **Use App:**
   - Create/view conversations via sidebar.
   - Chat for financial insights.

Ensure all services/APIs are active for full functionality.


## Project Structure

1. [application.py](application.py) - Main Flask app for server setup and API routes.
2. [src/database.py](src/database.py) - Manages MongoDB operations for users and conversations.
3. [src/tools.py](src/tools.py) - Functions for fetching financial news and results.
4. [src/rate_limiter.py](src/rate_limiter.py) - Rate limiting based on user tiers.
5. [src/agent.py](src/agent.py) - Handles LLM interactions and tool calls.
6. [streamlit-app.py](streamlit-app.py) - Streamlit UI for chatbot interaction.
7. [requirements.txt](requirements.txt) - Python dependencies list.
8. [.gitignore](.gitignore) - Files and directories to ignore in Git.
9. [PROBLEM_STATEMENT.md](PROBLEM_STATEMENT.md) - Problem statement and requirements.


## Design choices

- **Flask:** Lightweight and easy to use for API development.
- **MongoDB:** NoSQL database for quick and easy storage.
- **OpenAI API:** as the language model of choice for chatbot interactions.
- **Rate Limiting:** Used in-memory for simplicity.
- **Streamlit:** Simple and interactive UI development, easy to prototype and quick to deploy.
- **Langchain:** Due to support for multiple language models and easy integration with tool/function calling.

Some more points:
- The streamlit app is interacting with the backend via API calls only. Hence, it can be hosted separately, and can be replaced with any framework (like Next.js) for a more robust frontend.
- API calls are stateless, and the conversation context is stored in the database. Identification is done via a user-id and conversation id, which can passed via the API.
- For now, we use a hardcoded user-id, because authentication/authorization was out of scope.
- The endpoints are not protected, but can be secured using JWT tokens.
- There's no cap on number of messages for a conversation session for now. That's because 128K context length of gpt-4o-mini is sufficient for most conversations.
- The token rate limiting is done in-memory, and can be extended to Redis for scalability and persistence.
- Prompt is kept simple for now, but Chain of Thought and reasoning can be used for better context handling.

## Future Improvements
1. Streaming can be enabled for real-time chat. Improves user experience.
2. Adding summarization of some kind for long context conversations.
3. SSO/email based login/registration process for users.
4. Using Redis for rate limiting to ensure persistence.
5. Automatic conversation naming and manual renaming support (just like chatgpt).
