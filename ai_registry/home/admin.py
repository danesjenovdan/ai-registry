from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import AreaTag, Link, RegistryEntry


class LinkAdmin(admin.TabularInline):
    model = Link
    extra = 0


class RegistryEntryAdmin(admin.ModelAdmin):
    inlines = [LinkAdmin]
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "name",
                    "purpose",
                    "description",
                    # "links",
                    "time_in_use",
                    "institution",
                    "areas",
                    "tags",
                    "developers",
                    "license_duration",
                ]
            },
        ),
        (
            _("CENA"),
            {
                "fields": [
                    "cost",
                    "cost_comment",
                ]
            },
        ),
        (
            _("ANALIZE"),
            {
                "fields": [
                    "human_rights_analysis_done",
                    "human_rights_analysis_comments",
                    "personal_data_analysis_done",
                    "personal_data_analysis_comments",
                ]
            },
        ),
        (
            _("INTERNO"),
            {
                "fields": [
                    "comments",
                ]
            },
        ),
    ]


admin.site.register(RegistryEntry, RegistryEntryAdmin)
admin.site.register(AreaTag)
