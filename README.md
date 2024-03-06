# Stock Tracker

<p align="left">
    <a href="https://github.com/abeltavares/StockTracker">
        <img src="https://img.shields.io/badge/GitHub-Repository-blue?logo=github" alt="GitHub Repository">
    </a>
    <a href="https://www.djangoproject.com/">
        <img src="https://img.shields.io/badge/Django-5.0-blue?logo=django" alt="Django">
    </a>
    <a href="https://www.python.org/">
        <img src="https://img.shields.io/badge/Python-3.10-blue?logo=python" alt="Python">
    <a href="https://opensource.org/licenses/MIT">
        <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License">
    </a>        
    </a>
</p>

Stock Tracker is a web application built with Django and Python. It allows users to track the price of stocks in real-time. The application uses the Finnhub API to fetch the latest stock prices.

![demo](assets/stocktracker.gif)

## Features

- **User Registration and Authentication**
    - Users can register and login to the application. 

- **Stock Tracking**
    - Users can add stocks to their portfolio and track their prices in real-time

- **Stock Deletion** 
    - Users can remove stocks from their portfolio.

## Project Structure

The project is structured as a standard Django project with a single application `finnhub_app`. Here is a brief overview of the important files and directories in the project:

- `finnhub_app/`: This directory contains the Django application.

    - `admin.py`: This file is used to define the admin interface.

    - `apps.py`: This file is used to configure the Django application.

    - `forms.py`: This file contains the form for user registration.

    - `models.py`: This file defines the database models for the application.

    - `services.py`: This file contains the service layer functions, including `get_stock_data`, which encapsulates the logic for calling the Finnhub API.


    - `tests.py`: This file is used to write tests for the application.

    - `urls.py`: This file defines the URL routes for the application.

    - `views.py`: This file contains the view functions for the application.

    - `templates/`: This directory contains the HTML templates for the application.

- `finnhub_project/`: This directory contains the Django project settings.

    - `settings.py`: This file contains the settings for the Django project.

    - `urls.py`: This file defines the URL routes for the project.

    - `wsgi.py` and `asgi.py`: These files are used for deploying the application.

    - `manage.py`: This is a command-line utility that lets you interact with the Django project.

## Application Architecture

**User Registration and Authentication**:
    The user interacts with the registration or login page. The UI sends a request to the Django application, which validates the user's credentials and logs them in. The application uses Django's built-in authentication system. When a user registers or logs in, the user's information is stored in the Django's built-in User model. The registration and login forms are handled in `forms.py`, and the views for these forms are in `views.py`.

**Stock Tracking**:
    The user adds a stock to their portfolio through the UI. The UI sends a request to the Django application, which validates the stock symbol and adds the stock to the database. When a user wants to track a stock, they enter the stock symbol in the form on the `stocks.html` page. This triggers a POST request to the `fetch_stock_data` view in `views.py`.

**Fetching Stock Data**:
    The `fetch_stock_data` view uses the `get_stock_data` function from the service layer to get the latest stock prices from the Finnhub API. This function includes security checks such as input validation and exception handling to ensure the application is robust and secure. The API key for Finnhub is stored in the `.env` file and loaded into the settings using the `dotenv` package. The Finnhub API returns the current price of the stock.

**Storing Stock Data**:
    The application retrieves the stock data from the database and sends it to the UI, which displays the stocks to the user. The application stores the stock data in the `Stock` model defined in `models.py`. Each `Stock` instance has a symbol, price, and a timestamp of the last update. If the stock symbol already exists in the database, the application updates the price and the timestamp.

**User's Portfolio**:
    The user can remove a stock from their portfolio. This is handled by the `delete_stock` view in `views.py`, which removes the `PortfolioStock` instance linking the user's portfolio and the stock. Each user has a portfolio, which is a collection of stocks that the user is tracking. The portfolio is represented by the `Portfolio` model in `models.py`, which has a many-to-many relationship with the `Stock` model through the `PortfolioStock` model. When a user adds a stock to their portfolio, a new `PortfolioStock` instance is created linking the user's portfolio and the stock.

**Displaying Stock Data**:
    The `stocks.html` page displays the stocks in the user's portfolio. The page uses JavaScript to periodically get the latest stock data from the `stock_data_api` view in `views.py` and update the displayed prices.

**Deleting Stocks**:
    A user can remove a stock from their portfolio. This is handled by the `delete_stock` view in `views.py`, which removes the `PortfolioStock` instance linking the user's portfolio and the stock.

**Logout**:
    A user can log out of the application. This is handled by Django's built-in `LogoutView`.

The application's frontend is built with HTML and CSS, and it uses JavaScript for dynamic behavior. The HTML templates for the pages are stored in the `templates` directory in `finnhub_app`. The `home.html` template contains the common structure for all pages, and the other templates extend this base template. The JavaScript code in the `stocks.html` template fetches the latest stock data and updates the displayed prices.

```mermaid
graph TD; Client(Browser) --> Django_Web_Server; Django_Web_Server --> URL_Dispatcher; URL_Dispatcher --> Views; Views --> Service_Layer; Service_Layer --> Finnhub_API; Finnhub_API --> Service_Layer; Service_Layer --> Views; Views --> Models; Models --> Views; Views --> Templates; Templates --> Views; Views --> Django_Web_Server; Django_Web_Server --> Client(Browser);

```


## Setup and Installation

1. Clone the repository to your local machine.

2. Install the required dependencies using pip: `pip install -r requirements.txt`

3. Set up the environment variables in the `.env` file:

- `DB_USER`: The username for the PostgreSQL user.

- `DB_PASSWORD`: The password for the PostgreSQL user.

- `DB_PORT`: The port where the PostgreSQL server is listening.

- `DB_HOST`: The host where the PostgreSQL server is running on.

- `DB_NAME`: The name of the database.

- `FINNHUB_API_KEY`: The API key for the Finnhub API.

4. Run the Django migrations: `python manage.py migrate`

5. Start the Django development server: `python manage.py runserver`

## Usage

1. Open a web browser and navigate to `http://localhost:8000/`.

2. Register a new user or login with an existing user.

3. Add stocks to your portfolio by entering their symbol and clicking the `Add Stock` button.

4. The application will get the latest price for the stock and display it in the table.

5. You can remove stocks from your portfolio by clicking the `X` button next to the stock.

## Future Work and Considerations

The current implementation of the Stock Tracker application provides basic functionality for tracking real-time stock prices. However, there are several areas where the application could be improved and expanded:


**Real-Time Updates with WebSocket**:
    Currently, the application periodically fetches the latest stock data by sending HTTP requests. This could be improved by using Finnhub WebSocket, which would allow the server to push updates to the client in real-time. This would make the application more responsive and provide a better user experience.

**Expanded Stock Data**: 
    The application currently only tracks the price of stocks. This could be expanded to include more data, such as the stock's opening price, high and low prices, volume, and other relevant information. This would provide a more comprehensive overview of each stock's performance.

**International Market Support**: 
    The application currently supports US stocks. Support for international markets could be added for Enterprise clients.

**User Customization**: 
    Users could be allowed to customize their portfolio view, such as choosing which data points to display for each stock.

**Alerts and Notifications**: 
    The application could provide alerts and notifications when a stock reaches a certain price or changes by a certain percentage.

**Historical Data**: 
    The application could provide historical data for each stock, allowing users to see how the stock's price has changed over time.


For users interested in exploring historical data for stocks, check out the [Financial Dashboard App](https://abeltavares-financial-dashboard-app-app-ozm3yd.streamlit.app/) for a view of historical stock data analysis.

These are just a few suggestions for future work and considerations. The possibilities for expanding and improving the application are vast, and these improvements would enhance the user experience and the application's usefulness.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the [MIT License](LICENSE.txt).