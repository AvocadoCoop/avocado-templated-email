from __future__ import absolute_import, unicode_literals

from django.contrib import admin

from .models import EmailTemplate


def duplicate(self, request, queryset):
    for t in queryset:
        t.pk = None
        t.name = "{} Copy".format(t.name)
        t.save()


class EmailTemplateAdmin(admin.ModelAdmin):
    actions = (duplicate,)
    list_display = ('template_name', 'default_from', 'subject')


admin.site.register(EmailTemplate, EmailTemplateAdmin)
