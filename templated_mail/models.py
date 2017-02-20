from __future__ import absolute_import, unicode_literals
import os
import re

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.html import strip_tags


def plain_text_from_html(html):
    last_blank = False
    output = []
    for line in strip_tags(html).splitlines():
        line = line.strip()
        if not line:
            if not last_blank:
                output.append(line)
                last_blank = True
            else:
                continue
        else:
            output.append(line)
            last_blank = False
    return os.linesep.join(output)


include_re = re.compile(r"^%%(?P<name>.+)%%$")


def pre_render(template_string):
    rendered = []
    for line in template_string.split('\n'):
        line = line.strip()
        if not line.startswith("%%"):
            rendered.append(line)
            continue

        match = include_re.match(line)
        if match is None:
            rendered.append(line)
            continue

        template_name = match.group('name').strip()
        try:
            sub_template = EmailTemplate.objects.get(template_name=template_name)
        except EmailTemplate.DoesNotExist:
            rendered.append("{} -- No Email Template found this name".format(line))
            continue
        else:
            pre_rendered = pre_render(sub_template.html_prerendered())
            rendered.append(pre_rendered)

    return '\n'.join(rendered)


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

    def html_prerendered(self):
        return pre_render(self.html)

    def get_plain_text(self):
        if self.plain_text == '':
            return plain_text_from_html(self.html_prerendered())
        return self.plain_text

    def get_absolute_url(self):
        return reverse('templated_preview', args=[str(self.id)])

    def __str__(self):
        return self.template_name
