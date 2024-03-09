import os
from jsonschema import ValidationError
import requests

def get_stock_data(symbol):
    """
    Retrieves stock data for a given symbol.

    Args:
        symbol (str): The stock symbol to retrieve data for.

    Returns:
        tuple: A tuple containing the stock data and an error message (if any).
            The stock data is a dictionary containing information about the stock,
            and the error message is a string indicating any errors that occurred.

    Raises:
        ValidationError: If the stock symbol is invalid.

    """
    # Validate the symbol input
    if not symbol or not symbol.isalpha():
        raise ValidationError("Invalid stock symbol.")

    api_key = os.getenv("FINNHUB_API_KEY")
    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={api_key}"

    try:
        response = requests.get(
            url, timeout=5
        )  # Set a timeout to prevent hanging requests

        if response.status_code == 200:
            data = response.json()
            price = data.get("c")

            if price == 0:
                return None, "Invalid stock symbol."

            return data, None
        elif response.status_code == 429:
            return None, "Rate limit exceeded. Please try again later."
        else:
            return None, "Failed to get data"
    except requests.exceptions.RequestException as e:
        return None, f"Failed to get data: {str(e)}"
