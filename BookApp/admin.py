from django.contrib import admin
from .models import Book
from .models import Stage
from .models import Category
from .models import Language

class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title','author','isbn','updateDate', 'order')
    list_display_links = ('id', 'title','author','isbn','updateDate', 'order')

admin.site.register(Book, BookAdmin)


class StageAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')

admin.site.register(Stage, StageAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')

admin.site.register(Category, CategoryAdmin)


class LanguageAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')

admin.site.register(Language, LanguageAdmin)