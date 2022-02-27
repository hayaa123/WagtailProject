"""
Blog listing and blog detail pages
"""


from multiprocessing import context
from re import template
from django.db import models
from django.shortcuts import render

from wagtail.core.models import Page
from streams import blocks
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route

# Create your models here.


class BlogListingPage(RoutablePageMixin, Page):
    """
    List all blog detail pages 
    """
    template = "blog/blog_listing_page.html"
    custom_title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text="Blogs list title",
    )

    def get_context(self, request, *args, **kwargs):
        """
        adding custom stuff to our context
        """
        context = super().get_context(request, *args, **kwargs)
        context['posts'] = BlogDetailPage.objects.live().public()
        # context['text123']= "hello"
        return context
    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
    ]

    @route(r"^latest/$")
    def latest_blog_posts(self, request, *args, **kwargs):
        context = self.get_context( request, *args, **kwargs)
        context["latest_posts"]= BlogDetailPage.objects.live().public()[:1]
        return render(request, "blog/latest_posts.html", context)
    def get_sitemap_urls(self, request=None):
        sitemap = super().get_sitemap_urls(request)
        sitemap.append(
            {
                "location": self.full_url + self.reverse_subpage("latest_blog_posts"),
                "lastmod": (self.last_published_at or self.latest_revision_created_at),
                "priority": 0.9,
            }
        )
        return sitemap
class BlogDetailPage (Page):
    """
    blog detail page
    """
    template = "blog/blog_detail_page.html"
    custom_title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text="Blogs list title",
    )
    blog_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=False,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    content = StreamField(
        [
            ("title_and_text", blocks.TitleAndTextBlock()),
            ("full_richtext", blocks.RichTextBlock()),
            ("simple_richtext", blocks.SimpleRichTextBlock()),
            ("card", blocks.CardBlock()),
            ("cta", blocks.CTABlock())
        ],
        null=True,
        blank=True
    )

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
        ImageChooserPanel("blog_image"),
        StreamFieldPanel("content")
    ]
