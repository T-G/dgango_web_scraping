from django.db import models

# Create your models here.
class Search(models.Model):
    search_text = models.CharField(max_length=500)
    created_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return '{}'.format(self.search_text)
    
    class Meta:
        verbose_name_plural = 'Searches'
