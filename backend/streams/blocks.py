"""
Streamfield live in here
"""
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.contrib.table_block.blocks import TableBlock 
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.contrib.typed_table_block.blocks import TypedTableBlock


class HeaderItemBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, max_length=255)
    internal_url = blocks.PageChooserBlock(required=False)
    external_url =  blocks.URLBlock(required=False, help_text="If the internal_url above is selected there is no need to fill this field") 
    items = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("title", blocks.CharBlock(required=True, max_length=50)),
                ("internal_url", blocks.PageChooserBlock(required=False)),
                ("external_url", blocks.URLBlock(required=False,
                 help_text="If the internal_url above is selected there is no need to fill this field"))
            ]
        )
    )

    class Meta:
        template = "streams/header_items.html"
        icon = "edit"
        label = "Header Items"


class RawHTMLBlockTest(blocks.StructBlock):
    title = blocks.CharBlock(required=True, max_length=255, help_text='add the section title')
    table = blocks.RawHTMLBlock(required=True, min_length=100)
    class Meta:
        template = "streams/richtext_block.html"
        icon = "edit"
        label = "Full RichText"

class DemoStreamBlock(blocks.StreamBlock):
    title = blocks.CharBlock()
    paragraph = blocks.RichTextBlock()
    table = TypedTableBlock([
        ('text', blocks.CharBlock()),
        ('numeric', blocks.FloatBlock()),
        ('rich_text', blocks.RichTextBlock()),
        ('image', ImageChooserBlock())
    ])

class TitleAndTextBlock(blocks.StructBlock):
    """
    title and text
    """

    title = blocks.CharBlock(required=True, help_text="title", max_length=100)
    text = blocks.TextBlock(
        required=True, help_text="the text content goes here")
    file = DocumentChooserBlock(required=False, help_text='import the file')
    

    class Meta:
        template = "streams/title_and_text_Block.html"
        icon = "edit"
        label = "Title and text"


class RichTextBlock(blocks.RichTextBlock):
    """
    Richtext with all the features
    """
    class Meta:
        template = "streams/richtext_block.html"
        icon = "edit"
        label = "Full RichText"

class CardBlock(blocks.StructBlock):
    """
    Cards (image+text+button)
    """
    title = blocks.CharBlock(
        required=True, help_text="enter the title of thecards field here")
    cards = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("image", ImageChooserBlock(required=True)),
                ("title", blocks.CharBlock(required=True, max_length=50)),
                ("text", blocks.TextBlock(required=True, max_length=200)),
                ("button_page", blocks.PageChooserBlock(required=False)),
                ("button_url", blocks.URLBlock(required=False,
                 help_text="If the button page above is selected there is no need to fill this field"))
            ]
        )
    )

    class Meta:
        template = "streams/cards.html"
        icon = "placeholder"
        label = "Somthing Cards"


class SimpleRichTextBlock(blocks.RichTextBlock):
    """
    Richtext with limited features
    """

    def __init__(self, required=True, help_text=None, editor='default', features=None, validators=(), **kwargs):
        super().__init__(**kwargs)
        self.features = [
            "bold",
            "italic",
            "link"
        ]

    class Meta:
        template = "streams/richtext_block.html"
        icon = "edit"
        label = "Simple RichText"

class CTABlock(blocks.StructBlock):
    """
    A simple call to action section
    """
    title = blocks.CharBlock(required=True , max_length=50)
    text = blocks.RichTextBlock(required=True , features=["bold","italic"])
    button_page = blocks.PageChooserBlock(required=False)
    button_url = blocks.URLBlock(required=False)
    button_text = blocks.CharBlock(required=True,default="Learn More",max_length=20)

    class Meta:
        template = "streams/cta_block.html"
        icon = "placeholder"
        label = "Call to action "

class LinkStructValue(blocks.StructValue):
    """
    additional logic for our urls
    rather than add the logic in template if-else we can put the logic in python and pass 
    it to the Meta calss of the block as 'value_class' attribute then give it the logic class

    logic class should be inhirit from 'blocks.StructValue'
    """
    def url(self):
        button_page = self.get('button_page')
        button_url = self.get('button_url')
        if button_page:
            return button_page.url
        elif button_url:
            return button_url

        return None

class ButtonBlock(blocks.StructBlock):
    """
    an external or internal url
    """
    button_page = blocks.PageChooserBlock(required=False, help_text='If selected, this url will be used first')
    button_url = blocks.URLBlock(required=False, help_text='If added, this url will be used secondarily to the button page')

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        # context['latest_blogs'] = BlogDetailPage.objects.live.public()[:3]
        return context

    class Meta:  
        template = "streams/button_block.html"
        icon = "placeholder"
        label = "Single Button"
        value_class = LinkStructValue # we add this when we want to transfer the logic from template to python