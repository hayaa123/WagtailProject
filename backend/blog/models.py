"""
Blog listing and blog detail pages
"""

from django import forms
from django.core.paginator import EmptyPage, PageNotAnInteger,Paginator
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
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
from wagtail.api import APIField

from streams import blocks

from rest_framework.fields import Field
# Create your models here.

class ImageSerializedField(Field):
    """A custom serializer used in Wagtails v2 API."""

    def to_representation(self, value):
        """Return the image URL, title and dimensions."""
        return {
            "url": value.file.url,
            "title": value.title,
            "width": value.width,
            "height": value.height,
        }

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

    @property
    def author_name (self):
        return self.author.name    
    @property
    def author_website (self):
        return self.author.website   
    @property
    def author_image (self):
        return self.author.image
    # we added this property to expose more information from the author 
    # since the author is django model we should add the properties we want here 
    # because django dont have api_fields attribute 

    api_fields =[
        APIField("author_name")  ,
        APIField("author_website"),  
        # APIField("author_image",serializer=ImageSerializedField) ,# not working 
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
    # api_fields = [
    #     APIField("name")


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
        all_posts = BlogDetailPage.objects.live().public().order_by("-first_published_at")
        paginator = Paginator(all_posts,2)
        page= request.GET.get("page") 
        # addind another param into url by passing the name 
        name = request.GET.get("name")
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        context["posts"] = posts
        context ["name"] = name
        context["categories"] = BlogCategory.objects.all
        return context

        # context['posts'] = BlogDetailPage.objects.live().public() # this will display theparent and its children
        # we can just display the blog detail page without its children using BlogDetailPage.objects.live().exact_type(BlogDetailPage)
        # we can just display its children using BlogDetailPage.objects.live().not_exact_type(BlogDetailPage)
        # we can also select any page in its own using  BlogDetailPage.objects.live().exact_type(ArticleBlog)
       
    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
    ]

    @route(r"^year/(\d+)/(\d+)/",name="blogs_by_year")
    def blogs_by_year(self,request,year,month):
        # the year argument is to get access to the slug that been written in the url
        
        context = self.get_context(request)
        print(year)
        print(year)
        print(year)
        print(month)
        print(month)
        return render(request, "blog/latest_posts.html", context)


    @route(r"^category/(?P<cat_slug>[-\w]*)/$",name="category_view")
    def category_view(self, request, cat_slug):
        """Find blog posts based on a category."""
        context = self.get_context(request)

        try:
            # Look for the blog category by its slug.
            category = BlogCategory.objects.get(slug=cat_slug)
            
        except Exception:
            # Blog category doesnt exist (ie /blog/category/missing-category/)
            # Redirect to self.url, return a 404.. that's up to you!
            category = None

        if category is None:
            # This is an additional check.
            # If the category is None, do something. Maybe default to a particular category.
            # Or redirect the user to /blog/ ¯\_(ツ)_/¯
            pass
    
        context["latest_posts"] = BlogDetailPage.objects.live().public().filter(categories__in=[category])
        # Note: The below template (latest_posts.html) will need to be adjusted
        return render(request, "blog/latest_posts.html", context)
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
    
    api_fields =[
          APIField("blog_authors")  
        ]

    # def save(self,*args, **kwargs):

    #     key = make_template_fragment_key(
    #         "blog_post_preview",
    #         [self.id])
    #     cache.delete(key)
        # key = make_template_fragment_key(
        #     "navigation",
        #     )
        # cache.delete(key)
        # return super().save(*args,**kwargs) 
        # the save comes from  page model
        # here we can put the lines we want to render 
        # when saving these model  
        




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
