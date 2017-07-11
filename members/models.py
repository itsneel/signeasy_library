
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from jsonfield import JSONField


class Member(models.Model):

    user = models.OneToOneField(User, related_name='member', null=True)
    name = models.CharField(max_length=255, null=False)
    extra_info = JSONField(default={})
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    def mark_as_delete(self):
        self.is_active = False
        self.save()

    def delete(self):
        self.mark_as_delete()

