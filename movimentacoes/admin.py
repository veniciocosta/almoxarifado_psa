from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Produto, Movimentacao

# Register your models here.
admin.site.register(Produto)
admin.site.register(Movimentacao)