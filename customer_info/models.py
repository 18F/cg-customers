from django.contrib import admin
from django.db import models
from djmoney.models.fields import MoneyField

class Comment(models.Model):
    """
    Common comment model.
    """
    class Meta:
        abstract = True
    def __str__(self):
        return 'Date: {} | Comment: {}'.format(self.created_on, self.note)
    note = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

class AgreementComment(Comment):
    agreement = models.ForeignKey('Agreement')

class Agreement(models.Model):
    name = models.CharField(max_length=64, verbose_name="Agreement Name")
    mb_number = models.CharField(max_length=64, verbose_name="MB Number")
    start_date = models.DateField(verbose_name="Period Of Performance Start Date")
    end_date = models.DateField(verbose_name="Period Of Performance End Date")
    agreement_close_date = models.DateField(verbose_name="Agreement Close Date", blank=True, null=True)

    def __str__(self):
        return self.mb_number

class Package(models.Model):
    package_name = models.CharField(max_length=64)
    monthly_price = MoneyField(max_digits=12, decimal_places=2, default_currency='USD')

    def __str__(self):
        return 'Package: {}'.format(self.package_name)

class PackageHistory(models.Model):
    org = models.ForeignKey('Org')
    package_type = models.ForeignKey('Package')
    start_date = models.DateField(verbose_name="Package Effective Start Date")
    end_date = models.DateField(verbose_name="Package Effective End Date", null=True)

    def __str__(self):
        return 'Package: {} starting on {}'.format(self.package_type.package_name, self.start_date)

class QuotaHistory(models.Model):
    org = models.ForeignKey('Org')
    name = models.CharField(verbose_name="Quota Name", max_length=128)
    quota_memory_limit = models.PositiveIntegerField(verbose_name="Quota Memory Limit (in GB)")
    start_date = models.DateField(verbose_name="Quota Effective Start Date", help_text="")
    end_date = models.DateField(verbose_name="Quota Effective End Date", null=True)

    def __str__(self):
        return 'Quota: {}GB starting on {}'.format(self.quota_memory_limit, self.start_date)

class Org(models.Model):
    name = models.CharField(max_length=128, verbose_name="Org Name")
    agreement = models.ForeignKey('Agreement', null=True, verbose_name="Agreement")
    system_owner = models.CharField(max_length=64, verbose_name="System Owner")
    billing_choices = (
        ('active funding agreement', 'This is an org with an active funding agreement'),
        ('tts internal & no funding', 'This is an org serving TTS internal purposes with no funding agreement'),
        ('cloud.gov internal & no funding', 'This is an org for cloud.gov internal purposes, so it does not have a funding agreement'),
        ('misc. unbilled', 'This is unbilled for some other reason approved by the BU and documented in comments below'),
    )
    billing = models.CharField(max_length=32, verbose_name='Billing', choices=billing_choices, default='active funding agreement')

    def __str__(self):
        return 'Org: {}'.format(self.name)

class OrgComment(Comment):
    org = models.ForeignKey('Org')
