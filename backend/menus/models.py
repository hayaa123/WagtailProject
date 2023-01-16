from django.db import models
from django_extensions.db.fields import AutoSlugField
from wagtail.core.models import Page , Orderable
from wagtail.admin.edit_handlers import (
    MultiFieldPanel,
    FieldPanel,
    InlinePanel,
    PageChooserPanel
)
from wagtail.core.fields import (
    StreamField)
from wagtail.core.fields import RichTextField

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.snippets.models import register_snippet 
from streams import blocks

@register_snippet
class Header(ClusterableModel):
    title = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='title', editable=True)
    items = StreamField([
        ('header_items', blocks.HeaderItemBlock())
    ],
    null = True,
    blank = True
    )

    panels = [

        MultiFieldPanel(
            [
              FieldPanel("title"),
              FieldPanel("slug"),  
              FieldPanel("items"),  
            ] , heading = "header"
        )
    ]

    def __str__(self) -> str:
        return self.title




#-------------------------------------------------
@register_snippet
class Menu(ClusterableModel):
    title = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='title', editable=True)

    panels = [

        MultiFieldPanel(
            [
              FieldPanel("title"),
              FieldPanel("slug")   
            ] , heading = "menu"
        ),
        InlinePanel("menu_item", label= "Menu Item")
    ]

    def __str__(self) -> str:
        return self.title

class MenuItem(Orderable):
    link_title = models.CharField(
        blank = True,
        null = True,
        max_length=50
    )
    link_url = models.CharField(
        max_length=500,
        blank = True,
    )
    link_page = models.ForeignKey(
        "wagtailcore.Page",
        null = True ,
        blank = True,
        on_delete=models.CASCADE,
        related_name = "+"
    ) 

    items = StreamField([
        ('header_items', blocks.HeaderItemBlock())
    ],
    null = True,
    blank = True
    )
      
    open_in_new_tab = models.BooleanField(default=False)
    
    page = ParentalKey("Menu", related_name = "menu_item")

    panels = [
        FieldPanel ("link_title"),
        FieldPanel ("link_url"),
        FieldPanel("items"),
        PageChooserPanel ("link_page"),
        FieldPanel ("open_in_new_tab"),
    ]

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        elif self.link_url :
            return self.link_url
        else :
            return "#"

    @property
    def title (self):
        if self.link_page and not self.link_title:
            return self.link_page.title
        elif self.link_title:
            return self.link_title
        return "Missing Title"
        
#-------------------------

@register_snippet
class Footer(ClusterableModel):
    main_address1_english = models.CharField(max_length=255 ,null=True, blank=True)
    main_address1_arabic = models.CharField(max_length=255 ,null=True, blank=True)
    address2_english = models.CharField(max_length=255 ,null=True, blank=True)
    address2_arabic = models.CharField(max_length=255 ,null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=False, help_text='add school email')
    phone_number = models.CharField(max_length=50, blank=True)

    panels = [

        MultiFieldPanel(
            [
              FieldPanel("main_address1_english"),
              FieldPanel("main_address1_arabic"),  
              FieldPanel("address2_english"),  
              FieldPanel("address2_arabic"),  
              FieldPanel("email"),  
              FieldPanel("phone_number"),  
            ] , heading = "header"
        ),
        InlinePanel("school_item", label= "School Data")
    ]

    def __str__(self) -> str:
        return f'footer {self.id}'

class SchoolsItem(Orderable):
    title = models.CharField(max_length=150, null=False, blank=False)
    link_page = models.ForeignKey(
        "wagtailcore.Page",
        null = False ,
        blank = False,
        on_delete=models.CASCADE,
        related_name = "+"
    ) 
    footer = ParentalKey("Footer", related_name = "school_item")

    panels = [
        FieldPanel ("title"),
        PageChooserPanel ("link_page"),
    ]