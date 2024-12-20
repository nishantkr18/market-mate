import requests
from typing import List, Dict, Any

tools: List[Dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "get_financial_news",
            "description": "Fetch financial news for a specific company on a given date. Use this to provide users with the latest news headlines and descriptions related to a company.",
            "parameters": {
                "type": "object",
                "properties": {
                    "company_name": {
                        "type": "string",
                        "description": "The name of the company for which to fetch news.",
                    },
                    "date": {
                        "type": "string",
                        "description": "The date for which to fetch the news, in YYYY-MM-DD format.",
                    },
                },
                "required": ["company_name", "date"],
                "additionalProperties": False,
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_quarterly_financial_results",
            "description": "Fetch quarterly financial results for a specific company. Use this to provide users with financial metrics and documents related to a company's quarterly performance.",
            "parameters": {
                "type": "object",
                "properties": {
                    "company_name": {
                        "type": "string",
                        "description": "The name of the company for which to fetch financial results.",
                    },
                    "quarter": {
                        "type": "string",
                        "description": "The quarter for which to fetch the financial results, e.g., 'Q1 2023'.",
                    },
                },
                "required": ["company_name", "quarter"],
                "additionalProperties": False,
            },
        }
    }
]


def get_financial_news(company_name: str, date: str) -> Dict[str, Any]:
    """
    Fetch financial news for a specific company on a given date.

    Args:
        company_name (str): The name of the company for which to fetch news.
        date (str): The date for which to fetch the news, in YYYY-MM-DD format.

    Returns:
        Dict[str, Any]: A dictionary containing the company name and a list of news articles, each with a headline, description, date, and source.
    """
    # url = "https://dummyfinancialapi.com/news"
    # payload = {
    #     "company_name": company_name,
    #     "date": date
    # }
    # headers = {
    #     "Content-Type": "application/json"
    # }

    # response = requests.post(url, json=payload, headers=headers)

    # if response.status_code == 200:
    #     return response.json()
    # else:
    #     return {
    #         "error": f"Failed to fetch news. Status code: {response.status_code}",
    #         "details": response.text
    #     }
    return {
        "company_name": company_name,
        "news": [
            {
                "headline": f"{company_name} announces record profits!",
                "description": f"{company_name} has achieved record profits for the fiscal year.",
                "date": date,
                "source": "Financial Times"
            },
            {
                "headline": f"{company_name} partners with TechCorp.",
                "description": f"{company_name} has entered a strategic partnership with TechCorp to enhance market presence.",
                "date": date,
                "source": "Bloomberg"
            }
        ]
    }


def get_quarterly_financial_results(company_name: str, quarter: str) -> Dict[str, Any]:
    """
    Fetch quarterly financial results for a specific company.

    Args:
        company_name (str): The name of the company for which to fetch financial results.
        quarter (str): The quarter for which to fetch the financial results, e.g., 'Q1 2023'.

    Returns:
        Dict[str, Any]: A dictionary containing the company name, quarter, valuation ratios, and links to financial documents.
    """
    # url = "https://dummyfinancialapi.com/results"
    # payload = {
    #     "company_name": company_name,
    #     "quarter": quarter,
    #     "api_key": api_key
    # }
    # headers = {
    #     "Content-Type": "application/json"
    # }

    # response = requests.post(url, json=payload, headers=headers)

    # if response.status_code == 200:
    #     return response.json()
    # else:
    #     return {
    #         "error": f"Failed to fetch quarterly financial results. Status code: {response.status_code}",
    #         "details": response.text
    #     }
    return {
        "company_name": company_name,
        "quarter": quarter,
        "valuation_ratios": {
            "pe_ratio": 25.4,
            "pb_ratio": 3.8
        },
        "files": {
            "balance_sheet_excel": "https://dummyfinancialapi.com/files/balance_sheet.xlsx",
            "analyst_call_transcript_doc": "https://dummyfinancialapi.com/files/analyst_call_transcript.docx"
        }
    }
