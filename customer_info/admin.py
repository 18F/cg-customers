from django.contrib import admin
from django.core import urlresolvers
from django.utils.html import format_html
from reversion.admin import VersionAdmin
from .models import Agreement, AgreementComment, Org, OrgComment, Package, PackageHistory, QuotaHistory

class CommentInline(admin.TabularInline):
    """
    The base class for all comment inline classes.
    """
    extra = 0

class AgreementCommentInline(CommentInline):
    model = AgreementComment

@admin.register(Agreement)
class AgreementAdmin(admin.ModelAdmin):
    inlines = [AgreementCommentInline]
    list_display_links = ('name', 'mb_number')
    list_display = [f.name for f in Agreement._meta.fields if f.name != "id"]

@admin.register(Package)
class PackageAdmin(VersionAdmin):
    list_display = ('package_name', 'monthly_price',)

class PackageHistoryInline(admin.TabularInline):
    model = PackageHistory
    verbose_name = "Package History"
    verbose_name_plural = "Package History"
    extra = 1

class QuotaHistoryInline(admin.TabularInline):
    model = QuotaHistory
    verbose_name = "Quota History"
    verbose_name_plural = "Quota History"
    extra = 1

class OrgCommentInline(CommentInline):
    model = OrgComment

@admin.register(Org)
class OrgAdmin(VersionAdmin):
    list_display = ('name', 'system_owner', 'agreement_mb_number',)
    inlines = [PackageHistoryInline, QuotaHistoryInline, OrgCommentInline,]
    search_fields = ('name', 'system_owner', 'agreement__mb_number',)
    def agreement_mb_number(self, obj):
        link = urlresolvers.reverse('admin:customer_info_agreement_change', args=[obj.agreement_id])
        return format_html('<a target="_blank" href="{}">{}</a>', link, obj.agreement) if obj.agreement else None
