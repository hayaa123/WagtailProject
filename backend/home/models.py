from pyexpat import features
from tabnanny import verbose
from django.db import models
from django.shortcuts import render
from wagtail.api import APIField
from wagtail.admin.edit_handlers import (FieldPanel ,
    PageChooserPanel,
    StreamFieldPanel,
    InlinePanel,
    MultiFieldPanel)
from wagtail.core.models import Page , Orderable
from wagtail.core.fields import (
    RichTextField,
    StreamField)
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin ,route



from streams import blocks
from modelcluster.fields import ParentalKey


class HomePageCaroselImages(Orderable):
    """Between 1 and 5 images in the home page carosel """

    page = ParentalKey("home.homePage",related_name = "carosel_images")
    carosel_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    

    panels = [
        ImageChooserPanel("carosel_image")
    ]
    api_fields=[
        APIField("carosel_image")
    ]

class HomePage(RoutablePageMixin,Page):
    """
    Home page model
    """
    templates ="templates/home/home_page.html"
    banner_title = models.CharField(max_length=100,blank=False,null=True)
    max_count = 1
    banner_subtitle =RichTextField(features=["bold","italic"])
    banner_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    banner_cta = models.ForeignKey(
        "wagtailcore.page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    content = StreamField(
        [
            ("title_and_text", blocks.TitleAndTextBlock()),
            ("full_richtext", blocks.RichTextBlock()),
            ("simple_richtext", blocks.SimpleRichTextBlock()),
            ("card",blocks.CardBlock()),
            ("cta",blocks.CTABlock()),
            ("doc", blocks.DocBlock()),
            ('doc2',blocks.Doc2Block())
        ],
        null=True,
        blank=True
    )

    api_fields = [
        APIField("banner_title"),
        APIField("banner_subtitle"),
        APIField("banner_image"),
        APIField("banner_cta"),
        APIField("carosel_images"),
        APIField("content"),
    ]

    content_panels = Page.content_panels +[
    MultiFieldPanel([
        FieldPanel("banner_title"),
        FieldPanel("banner_subtitle"),
        ImageChooserPanel("banner_image"),
        PageChooserPanel("banner_cta"),
    ],heading="Baner Options"), 

    MultiFieldPanel([
    InlinePanel("carosel_images",max_num=5,min_num=1,label="Image"),
    ],heading="Carosel Images"),

    StreamFieldPanel("content")
    ]

    class Meta :
        verbose_name = "Home Page"
        verbose_name_plural ="Home Pages"

    @route(r'^subscribe/$')
    def the_subscribe_page(self,request,*args,**kwargs):
        context = self.get_context(request,*args ,**kwargs)
        context["test"] = "hello world"
        return render(request , "home/subscribe.html",context)

# Inherit from PdfViewPageMixin
# class SimplePdfPage(PdfViewPageMixin, Page):
    
#     # you can create fields as you're used to, e.g. StreamField
#     content = StreamField([
#         # ("heading", blocks.CharBlock(form_classname="full title")),
#         ("text", blocks.RichTextBlock()),
#     ], blank=True)
    
#     # content panel for the CMS (same as always)
#     content_panels = Page.content_panels + [
#         StreamFieldPanel("content"),
#     ]
#     # ROUTE_CONFIG = [
#     #     ("pdf", r'^$'),
#     #     ("html", r'^html/$'),
#     # ]
    
    
#     # OPTIONAL: If you want to include a stylesheet
#     #stylesheets = ["css/your_stylesheet.css"]

# class PdfOnlyPage(PdfViewPageMixin, Page):

#     # PDF only
#     ROUTE_CONFIG = [
#         ("pdf", r'^$'),
#         ("html", None),
#     ]

# class HtmlAndPdfPage(PdfViewPageMixin, Page):

#     # HTML first
#     ROUTE_CONFIG = [
#         ("html", r'^$'),
#         ("pdf", r'^pdf/$'),
#     ]
    
# class HtmlAndPdfPage(PdfViewPageMixin, Page):
    
#     # PDF first
#     ROUTE_CONFIG = [
#         ("pdf", r'^$'),
#         ("html", r'^html/$'),
#     ]
    