from django.db import models
from wagtail.core.models import Page ,Orderable
from wagtail.admin.edit_handlers import (
    FieldPanel ,
    InlinePanel,
    StreamFieldPanel,
    )
from wagtail.core.fields import (
    StreamField)
from streams import blocks
from modelcluster.fields import ParentalKey
from wagtail.images.edit_handlers import ImageChooserPanel

# Create your models here.

# class PageWithSide(Page):    
#     content_panels = Page.content_panels +[

#         FieldPanel("title"),
#         InlinePanel('side',label='Side nav with its content')
        
# ]
    
    
# class SideWithContent(Orderable):
#     nav_title = models.CharField(max_length=200)
#     page = ParentalKey('PageWithSide',related_name='side')
#     content = StreamField(
#         [
#             ("title_and_text", blocks.TitleAndTextBlock()),
#             ("full_richtext", blocks.RichTextBlock()),
#             ("simple_richtext", blocks.SimpleRichTextBlock()),
#             ("card",blocks.CardBlock()),
#             ("cta",blocks.CTABlock()),
#             ("doc", blocks.DocBlock()),
#             ('doc2',blocks.Doc2Block())
#         ],
#         null=True,
#         blank=True
#     )
    
#     panels = [
#         FieldPanel('nav_title'),
#         FieldPanel("content"),
#     ]

class AdmissionPage(Page):
    subpage_types =[
        'page_with_side.NavSection'
    ]
    
    @property
    def menu(self):
        return self.get_parent().specific.menu
    


class NavSection(Page):
    template = 'page_with_side/nav_section.html'    
    nav_title = models.CharField(max_length=50)
    
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
    @property
    def menu(self):
        return self.get_parent().specific.menu
    
    def get_context(self, request, *args, **kwargs):
        context= super().get_context(request, *args, **kwargs)
        l= []
        for nav_item in self.get_siblings(inclusive=True):
            print(nav_item)
            # l.append({'icon': nav_item.nav_icon , 'title':nav_item.nav_title,"slug":nav_item.slug})
        context['nav_info'] = self.get_siblings(inclusive=True).specific
        return context
        
    parent_page_type=['page_with_side.AdmissionPage']
    subpage_types =[]
    content_panels = Page.content_panels +[        
        FieldPanel('nav_title'),
        StreamFieldPanel('content'),        
]
