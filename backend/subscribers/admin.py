
from .models import Subscriber
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    modeladmin_register
)
class SubscriberAdmin(ModelAdmin):
    """
    subscriber in the admin side 
    """

    model = Subscriber
    menu_label = "blog_subscribers"
    menu_icon ="pick"
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_dispaly = ("email","full_name")
    search_fields = ("email","full_name")
    
modeladmin_register(SubscriberAdmin)