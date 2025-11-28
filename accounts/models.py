# accounts/models.py
# ----------------------------------------------------------------------------------------------------

from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    # add custom fields here later (e.g., profile_picture, age)
    pass
