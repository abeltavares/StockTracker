"""
URL patterns for the Finnhub app.

This module defines the URL patterns for the Finnhub app, which is responsible for handling various web requests related to stock data.

The urlpatterns list contains instances of the path() function, which maps URL patterns to corresponding view functions or classes.

URL Patterns:
- "" (empty string): Maps to the home view function.
- "login/": Maps to the LoginView class with the login.html template.
- "logout/": Maps to the LogoutView class.
- "register/": Maps to the register view function.
- "stock-data/": Maps to the fetch_stock_data view function.
- "api/stock-data/": Maps to the stock_data_api view function.
- "delete-stock/": Maps to the delete_stock view function.

Note: The names specified in the name parameter are used to refer to these URLs in the Django templates or when generating URLs dynamically.
"""

from django.urls import path
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
)
from .views import *

urlpatterns = [
    path("", home, name="home"),
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", register, name="register"),
    path("stock-data/", fetch_stock_data, name="fetch_stock_data"),
    path("api/stock-data/", stock_data_api, name="stock_data_api"),
    path("delete-stock/", delete_stock, name="delete_stock"),
]
