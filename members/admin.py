from django.contrib import admin

from members import models


class MembersAdmin(admin.ModelAdmin):
    list_display = ('name', )

admin.site.register(models.Member, MembersAdmin)
