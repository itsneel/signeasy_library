
from django.db import IntegrityError
from django.forms.models import model_to_dict

from books import models
from books import exceptions
from common_exceptions import exceptions as common_exceptions
from members import mod as members_mod


def get_all_books():
    books = models.Book.objects.all()
    books_list = []
    for book in books:
        book = model_to_dict(book)
        books_list.append(book)
    return books_list


def add_or_update_book(sku, data={}):
    if not sku:
        raise exceptions.SkuNotpresetError
    try:
        book, created = models.Book.objects.get_or_create(sku=sku **data)
        if not created:
            # update the book
            book.name = data.get('name')
            book.description = data.get('description')
            book.total = data.get('total', 0)
            book.save()
    except IntegrityError:
        raise common_exceptions.RaceConditionIntegrityError
    return book, created


def issue_book(member_id, book_sku):
    books = models.objects.filter(sku=book_sku)
    if not books:
        raise exceptions.BookNotFoundError
    book = books[0]
    if not _can_issue_book(book):
        raise exceptions.BookCanNotBeIssuedError
    member = members_mod.get_member(member_id)
    obj = models.BookIssue.objects.create(member=member, book=book)
    return obj.is_active



def _get_issued_books_count(book):
    if not book:
        return 0
    return book.issued.objects.all().count()


def _can_issue_book(book):
    issued_books = _get_issued_books_count(book)
    return issued_books < book.total