from django.db import models

# Create your models here.
class IAA(models.Model):
    iaa_name = models.CharField(max_length=64, verbose_name="IAA Name")
    start_date = models.DateField(verbose_name="Agreement Start Date")
    end_date = models.DateField(verbose_name="Agreement End Date")

    def __str__(self):
        return 'IAA: {}'.format(self.iaa_name)
