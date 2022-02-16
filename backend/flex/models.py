"""
flexible page
"""

from django.db import models
from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel

class FlexPage (Page):
    template = "flex/flex_page.html"
    # content = StreamField()

    subtitle = models.CharField(max_length=100,blank=True , null=True)
    content_panels = Page.content_panels + [
        FieldPanel("subtitle")
    ]
    
    class Meta :
        verbose_name = "Flex Page"
        verbose_name_plural = "Flex Pages"