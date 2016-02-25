from __future__ import absolute_import, unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class EmailTemplate(models.Model):
    template_name = models.CharField(max_length=256)
    subject = models.CharField(max_length=256)
    default_from = models.CharField(
        max_length=128,
        blank=True,
        help_text="Optional. From in code passed into send takes precedence. DEFAULT_FROM used if available."
    )

    html = models.TextField()

    plain_text = models.TextField(blank=True, help_text="Optional. If blank generated from html")

    def __str__(self):
        return self.template_name
