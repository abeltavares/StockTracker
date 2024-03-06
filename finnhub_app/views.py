from django.http import JsonResponse
from django.shortcuts import redirect, render
from jsonschema import ValidationError
from .models import Stock
import requests
import os
from .models import Portfolio
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .services import get_stock_data


@login_required
def home(request):
    """
    Renders the home page for the authenticated user.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered stocks.html template with the user's portfolio.

    """
    user = request.user
    portfolio, created = Portfolio.objects.get_or_create(user=user)
    return render(request, "stocks.html", {"portfolio": portfolio})


def register(request):
    """
    User Registration form
    Args:
        request (POST): New user registered
    """
    form = UserRegistrationForm()
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserRegistrationForm()

    context = {"form": form}
    return render(request, "register.html", context)


@login_required
def delete_stock(request):
    """
    Deletes a stock from the user's portfolio.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: A JSON response indicating the success or failure of the operation.
    """
    if request.method == "POST":
        symbol = request.POST.get("symbol").upper()

        user = request.user
        portfolio, created = Portfolio.objects.get_or_create(user=user)

        try:
            stock = Stock.objects.get(symbol=symbol)
        except Stock.DoesNotExist:
            return JsonResponse(
                {"success": False, "error": "Stock not found"}, status=400
            )

        portfolio.stocks.remove(stock)

        return JsonResponse({"success": True})
    else:
        return JsonResponse(
            {"success": False, "error": "Invalid request method"}, status=400
        )


@login_required
def fetch_stock_data(request):
    """
    Fetches stock data for a given symbol and updates the user's portfolio.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: A JSON response containing the result of the operation.

    Raises:
        ValidationError: If there is an error validating the input.

    """
    if request.method == "POST":
        symbol = request.POST.get("symbol").upper()
        try:
            data, error = get_stock_data(symbol)

            if error:
                return JsonResponse({"error": error}, status=400)

            price = data.get("c")
            stock, created = Stock.objects.get_or_create(
                symbol=symbol, defaults={"price": price}
            )

            if not created:
                stock.price = price
                stock.save()

            user = request.user
            portfolio, created = Portfolio.objects.get_or_create(user=user)

            if not portfolio.stocks.filter(symbol=symbol).exists():
                portfolio.stocks.add(stock)
                return JsonResponse(
                    {"message": f"Stock {symbol} added to your portfolio."}
                )
            else:
                return JsonResponse(
                    {"error": f"Stock {symbol} is already in your portfolio."}
                )
        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)


@login_required
def stock_data_api(request):
    """
    API endpoint to fetch stock data for the user's portfolio.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: A JSON response containing the stock data.

    Raises:
        None

    """
    user = request.user
    try:
        portfolio = Portfolio.objects.get(user=user)
    except Portfolio.DoesNotExist:
        portfolio = Portfolio.objects.create(user=user)

    stocks = Stock.objects.filter(portfoliostock__portfolio=portfolio)

    data = [{"symbol": stock.symbol, "price": stock.price} for stock in stocks]
    return JsonResponse(data, safe=False)
