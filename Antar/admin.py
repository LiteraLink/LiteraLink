from django.contrib import admin

from Antar.models import Books, Person

# Register your models here.

admin.site.register(Person)
admin.site.register(Books)