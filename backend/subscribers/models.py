from django.db import models

# Create your models here.

class Subscriber (models.Model):
    """
    A subscribers model
    """

    email = models.CharField(blank=False,null=False,help_text="email adress",max_length=100)
    full_name = models.CharField(max_length=100 ,blank=False,null=False , help_text="first and last name ")

    def __str__(self):
        """
        string representation of this object 
        """
        return self.full_name