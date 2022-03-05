"""
Blog listing and blog detail pages
"""

from django import forms
from django.db import models
from django.shortcuts import render
from modelcluster.fields import ParentalKey ,ParentalManyToManyField
from wagtail.core.models import Page , Orderable
from streams import blocks
from wagtail.admin.edit_handlers import (
    FieldPanel,
    StreamFieldPanel,
    MultiFieldPanel,
    InlinePanel
)
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.core.fields import StreamField 
from wagtail.images.edit_handlers import ImageChooserPanel 
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.snippets.models import register_snippet
from streams import blocks
# Create your models here.

class BlogAuthorsOrderable(Orderable):
    """
    allow us to select one or more blog author
    """
    page = ParentalKey("blog.BlogDetailpage",related_name="blog_authors")
    author = models.ForeignKey(
        "blog.BlogAuthor",
        on_delete = models.CASCADE,
    )

    panels = [
        SnippetChooserPanel("author")
    ]

class BlogAuthor(models.Model):
    """
    Blog author for snippets
    """
    name = models.CharField(max_length=100)
    website = models.URLField(blank=True, null=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="+"
    )

    panels = [MultiFieldPanel(
        [
            FieldPanel("name"),
            ImageChooserPanel("image")
        ],
        heading="name and Image"
    ),
        MultiFieldPanel([
            FieldPanel("website")
        ],
        heading="link"
        )
    ]

    def __str__(self) -> str:
        return self.name
    class Meta :
        verbose_name = "Blog Author"
        verbose_name_plural = "Blog Authors"

register_snippet(BlogAuthor)


class BlogCategory(models.Model):
    """
    Blog category for a snippet
    """
    name = models.CharField(max_length=225)
    slug = models.SlugField(
        verbose_name="slug",
        max_length=255,help_text="A slug to identify posts by this categorie " ,
        allow_unicode=True)

    panels = [
        FieldPanel("name"),
        FieldPanel("slug")
    ] 

    def __str__(self) -> str:
        return self.name
    class Mata :
        verbose_name = "Blog Category"
        verbose_name_plural = "Blog Categories"
        ordering = ("name")
    

register_snippet(BlogCategory)

    

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
        context["categories"] = BlogCategory.objects.all
        return context
    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
    ]

    @route(r"^latest/$")
    def latest_blog_posts(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        context["latest_posts"] = BlogDetailPage.objects.live().public()[:1]
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
    categories = ParentalManyToManyField("blog.BlogCategory",blank=True)
    # def detail_(self, request, *args, **kwargs):
    #     return super().get_context(request, *args, **kwargs)
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
        StreamFieldPanel("content"),
        MultiFieldPanel(
        [
            InlinePanel("blog_authors",label="author",min_num=1,max_num=4)
        ],heading="Author"
        ),
        MultiFieldPanel(
        [
            FieldPanel("categories",widget = forms.CheckboxSelectMultiple)
        ],heading="Categories"
        )
    ]


# first subclass blog post page
class ArticleBlogPage(BlogDetailPage):
    """
    A subclass blog post page
    """
    template = "blog/article_blog_page.html"

    subtitle = models.CharField(
        max_length=100,
        blank=True,
        null=True)

    intero_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=True,
        null=True,
        on_delete = models.CASCADE,
    )

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
        FieldPanel('subtitle'),
        ImageChooserPanel("blog_image"),
        ImageChooserPanel("intero_image"),
        StreamFieldPanel("content"),
        MultiFieldPanel(
        [
            InlinePanel("blog_authors",label="author",min_num=1,max_num=4)
        ],heading="Author"
        ),
        MultiFieldPanel(
        [
            FieldPanel("categories",widget = forms.CheckboxSelectMultiple)
        ],heading="Categories"
        )
    ]

class VideoBlogPage(BlogDetailPage):
    """
    A video subclass page
    """

    youtube_video_id = models.CharField(max_length=100)


    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
        FieldPanel("youtube_video_id"),
        ImageChooserPanel("blog_image"),
        StreamFieldPanel("content"),
        MultiFieldPanel(
        [
            InlinePanel("blog_authors",label="author",min_num=1,max_num=4)
        ],heading="Author"
        ),
        MultiFieldPanel(
        [
            FieldPanel("categories",widget = forms.CheckboxSelectMultiple)
        ],heading="Categories"
        )
    ]
