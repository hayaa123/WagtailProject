from django.db import models
from wagtail.admin.edit_handlers import FieldPanel ,MultiFieldPanel
from wagtail.contrib.settings.models import BaseSetting,register_setting
# Create your models here.

@register_setting
class SocialMediaSettings(BaseSetting):
    """
    Social media setting for this blog website
    """

    facebook = models.URLField(blank=True,null=True,help_text="facebook url") 
    twitter = models.URLField(blank=True,null=True,help_text="twitter url")  
    youtube = models.URLField(blank=True,null=True,help_text="youtube url")

    panels = [
        MultiFieldPanel([
            FieldPanel("facebook"),
            FieldPanel("twitter"),
            FieldPanel("youtube"),

        ],heading="Social Media Setting")

    ]