from django.db import models
from django.contrib.auth.models import User


class Portfolio(models.Model):
    """
    Represents a user's portfolio.

    Attributes:
        user (User): The user who owns the portfolio.
        stocks (ManyToManyField): The stocks in the portfolio.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stocks = models.ManyToManyField("Stock", through="PortfolioStock")

    def __str__(self):
        return f"{self.user.username}'s Portfolio"


class PortfolioStock(models.Model):
    """
    Represents a stock in a portfolio.

    Attributes:
        portfolio (Portfolio): The portfolio that this stock belongs to.
        stock (Stock): The stock associated with this portfolio.
    """

    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    stock = models.ForeignKey("Stock", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("portfolio", "stock")
        verbose_name_plural = "Portfolio Stocks"


class Stock(models.Model):
    """
    Represents a stock in the system.

    Attributes:
        symbol (str): The symbol of the stock.
        price (Decimal): The price of the stock.
        last_updated (datetime): The last time the stock was updated.
    """

    symbol = models.CharField(max_length=10, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.symbol
