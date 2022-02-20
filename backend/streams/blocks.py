"""
Streamfield live in here
"""

from email.policy import default
import re
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


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

