from django.contrib import admin
from .models import User, Book



@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year', 'genre', 'availability')
    search_fields = ('title', 'author')



@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'role') 
    search_fields = ('username',)