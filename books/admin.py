from django.contrib import admin

from books import models


class BooksAdmin(admin.ModelAdmin):
    list_display = ('name', )

admin.site.register(models.Book, BooksAdmin)


class BookIssuesAdmin(admin.ModelAdmin):
    list_display = ('member', 'book', )

admin.site.register(models.BookIssue, BookIssuesAdmin)
