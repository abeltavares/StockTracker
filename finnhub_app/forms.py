from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

UserModel = get_user_model()


class UserRegistrationForm(UserCreationForm):
    """
    A form for user registration.

    This form extends the UserCreationForm provided by Django's authentication framework.
    It includes fields for username, password1, and password2.

    Attributes:
        model (UserModel): The user model to be used for registration.
        fields (list): The fields to be included in the form.

    """

    class Meta:
        model = UserModel
        fields = ["username", "password1", "password2"]
