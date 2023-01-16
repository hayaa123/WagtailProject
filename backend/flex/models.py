"""
flexible page
"""

from django.db import models
from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel ,MultiFieldPanel,InlinePanel
from streams import blocks


class FlexPage (Page):
    template = "flex/flex_page.html"
    content = StreamField(
        [
            ("title_and_text", blocks.TitleAndTextBlock()),
            ("full_richtext", blocks.RichTextBlock()),
            ("simple_richtext", blocks.SimpleRichTextBlock()),
            ("card",blocks.CardBlock()),
            ("cta",blocks.CTABlock()),
            # ("button",blocks.ButtonBlock())
        ],
        null=True,
        blank=True
    )

    subtitle = models.CharField(max_length=100, blank=True, null=True)
    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
        StreamFieldPanel("content"),
    
    ]

    @property
    def menu(self):
        return self.get_parent().specific.menu
    
    @property
    def footer(self):
        return self.get_parent().specific.footer
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['test_parent'] = self.get_parent().specific.menu
        return context
    class Meta:
        verbose_name = "Flex Page"
        verbose_name_plural = "Flex Pages"
