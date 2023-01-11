"""
Streamfield live in here
"""

from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.documents.blocks import DocumentChooserBlock

class TitleAndTextBlock(blocks.StructBlock):
    """
    title and text
    """

    title = blocks.CharBlock(required=True, help_text="title", max_length=100)
    text = blocks.TextBlock(
        required=True, help_text="the text content goes here")

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


class DocBlock(blocks.StructBlock):
    """
    A simple call to action section
    """
    title = blocks.CharBlock(required=True , max_length=50)
    doc = DocumentChooserBlock()
    print("doc_att: ", dir(doc))


    def get_context(self, request,*args,**kwargs):
        context= super().get_context(request,*args,**kwargs)
        # context ["doc_data"] = getattr(self.doc)
        context ["hello"] = "Hello"
        return context
    class Meta:
        template = "streams/doc.html"
        icon = "placeholder"
        label = "Call to action "



class LinkStructValue(blocks.StructValue):
    """
    additional logic for our urls
    """
    def url(self):
        button_page = self.get('button_page')
        button_url = self.get('button_url')
        if button_page:
            return button_page.url
        elif button_url:
            return button_url

        return None

# class ButtonBlock(blocks.StructBlock):
#     """
#     an external or internal url
#     """
#     button_page = blocks.PageChooserBlock(required=False, help_text='If selected, this url will be used first')
#     button_url = blocks.URLBlock(required=False, help_text='If added, this url will be used secondarily to the button page')

#     class Meta:  
#         template = "streams/button_block.html"
#         icon = "placeholder"
#         label = "Single Button"
#         value_class = LinkStructValue