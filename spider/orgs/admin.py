from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(
    [
        District,
        Category,
        EnterpriseNetwork,
        Merchandise,
        Enterprise,
        Merch
    ]
)
