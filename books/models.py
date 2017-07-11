
from django.db import models
from django.utils import timezone

from jsonfield import JSONField

from members import models as members_models


class Book(models.Model):

    sku = models.CharField(max_length=255, null=False, unique=True)
    name = models.CharField(max_length=255, null=False)
    description = models.BooleanField(default=True)
    total = models.IntegerField(default=0)
    extra_info = JSONField(default={})
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        index_together = (('sku', 'name'), )
        unique_together = (('sku', 'name'), )

    def __unicode__(self):
        return self.name

    def mark_as_delete(self):
        self.is_active = False
        self.save()

    def delete(self):
        self.mark_as_delete()


class BookIssue(models.Model):

    member = models.ForeignKey(members_models.Member, related_name='issued_books')
    book = models.ForeignKey(Book, related_name='issued')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        index_together = (('member', 'book'), )

    def __unicode__(self):
        return 'user: {}, book: {}'.format(self.member.user.username, self.book.name)

    def return_book(self):
        self.is_active = False
        self.save()
