from typing import List
from langchain_core.messages import SystemMessage, ToolMessage, HumanMessage, convert_to_openai_messages
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from src.rate_limiter import check_rate_limit
from src.database import get_conversation, update_conversation_history
from src.tools import get_financial_news, get_quarterly_financial_results, tools

# Load environment variables from a .env file
load_dotenv()


def get_answer_in_conversation(conversation_id: str, user_message: str) -> str:
    """
    Handles the process of sending a user message to a specific conversation and retrieving the AI's response.

    Args:
        conversation_id (str): The unique identifier for the conversation.
        user_message (str): The message from the user to be added to the conversation.

    Returns:
        str: The AI's response to the user's message. Returns None if the conversation is not found.
    """
    # Retrieve the conversation details from the database
    conversation = get_conversation(conversation_id)
    if conversation is None:
        return None

    # Extract the conversation history
    conv_hist = conversation.get("messages", [])

    # Append the user's message to the conversation history
    conv_hist.append(HumanMessage(user_message))

    # Generate the AI's response based on the updated conversation history
    conv_hist = get_answer(conv_hist)

    # Convert the conversation history to a format compatible with OpenAI
    conv_hist = convert_to_openai_messages(conv_hist)

    # Update the conversation in the database with the new messages
    update_conversation_history(conversation_id, conv_hist)

    # Return the latest AI response
    return conv_hist[-1]


def get_answer(conv_hist: List[dict]) -> List[dict]:
    """
    Generates an AI response based on the conversation history using a language model.

    Args:
        conv_hist (List[dict]): The current conversation history.

    Returns:
        List[dict]: The updated conversation history including the AI's response.
    """
    # Define the prompt for the AI model
    prompt = f"""You are MarketMate, an AI assistant specialized in answering questions related to financial markets. Your role is to provide accurate, concise, and user-friendly responses. Follow these guidelines:

1. Always respond within the context of financial markets, such as stock prices, company financials, economic trends, or investment strategies.
2. If a question is outside the financial domain, politely inform the user that you only handle financial market-related queries.
3. Use data-driven responses when applicable. If data is unavailable, indicate this to the user without guessing.
4. Your tone should be professional but approachable. Avoid overly technical jargon unless the user explicitly requests it.
5. If the user asks for specific financial data (e.g., quarterly results, valuation ratios), use the appropriate functions to fetch this data. For example, use get_quarterly_financial_results or get_financial_news as needed.
6. Always ensure compliance with the user's tier (e.g., Free, Tier-1) and provide simplified answers for free-tier users if required.

Example Interaction:
User: "What is the P/E ratio of Apple Inc.?"
Assistant: "The Price-to-Earnings (P/E) ratio of Apple Inc. is 28.7, based on the latest quarterly results. This measures how much investors are willing to pay for $1 of earnings."

If asked to perform a calculation or summarize information, do so accurately.

You are part of a secure application. Avoid discussing internal implementation details or confidential information.

"""

    total_tokens = 0

    # Initialize the language model with the specified model type
    llm = ChatOpenAI(model='gpt-4o-mini')

    # Bind the language model with the available tools
    llm_with_tools = llm.bind_tools(tools, strict=True)

    # Invoke the language model with the prompt and conversation history
    response = llm_with_tools.invoke([SystemMessage(prompt)] + conv_hist)
    total_tokens += response.usage_metadata['total_tokens']
    conv_hist.append(response)

    # Handle any tool calls made by the AI
    if response.tool_calls:
        for tool_call in response.tool_calls:
            print(tool_call)  # Log the tool call for debugging purposes
            selected_tool = {
                "get_financial_news": get_financial_news,
                "get_quarterly_financial_results": get_quarterly_financial_results
            }[tool_call["name"].lower()]
            tool_output = selected_tool(**tool_call["args"])
            conv_hist.append(ToolMessage(
                tool_output, tool_call_id=tool_call["id"]))

        # Re-invoke the language model after tool calls to get the final response
        response = llm_with_tools.invoke([SystemMessage(prompt)] + conv_hist)
        total_tokens += response.usage_metadata['total_tokens']
        conv_hist.append(response)

    # Update rate limit usage for the user
    check_rate_limit("nniishantkumar@gmail.com", "TPM", total_tokens)
    check_rate_limit("nniishantkumar@gmail.com", "TPD", total_tokens)

    # Return the updated conversation history
    return conv_hist
