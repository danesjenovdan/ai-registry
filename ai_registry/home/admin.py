from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from taggit.admin import Tag

from .models.registry_entry import Link, RegistryEntry, RegistryEntryInstitutionData
from .models.tags import AreaTag, GenericTag, InstitutionTag

# remove the default taggit.Tag model from the admin
admin.site.unregister(Tag)


class LinkAdminInline(admin.TabularInline):
    model = Link
    extra = 0


REGISTRY_ENTRY_INSTITUTION_DATA_ADMIN_FIELDSETS_INLINE = [
    (
        None,
        {
            "fields": [
                "institution",
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
        _("LICENCA"),
        {
            "fields": [
                "license_duration",
                "license_duration_comment",
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
        _("JAVNO NAROČILO"),
        {
            "fields": [
                "public_procurement",
                "public_procurement_number",
                "public_procurement_number_eu",
                "public_procurement_date",
                "contracting_institution",
            ]
        },
    ),
]

REGISTRY_ENTRY_INSTITUTION_DATA_ADMIN_FIELDSETS = [
    (
        None,
        {
            "fields": [
                "registry_entry",
                "institution",
            ]
        },
    ),
    *REGISTRY_ENTRY_INSTITUTION_DATA_ADMIN_FIELDSETS_INLINE[1:],
]


class RegistryEntryInstitutionDataAdminInline(admin.StackedInline):
    model = RegistryEntryInstitutionData
    extra = 0
    fieldsets = REGISTRY_ENTRY_INSTITUTION_DATA_ADMIN_FIELDSETS_INLINE


class RegistryEntryInstitutionDataAdmin(admin.ModelAdmin):
    fieldsets = REGISTRY_ENTRY_INSTITUTION_DATA_ADMIN_FIELDSETS


class RegistryEntryAdmin(admin.ModelAdmin):
    inlines = [RegistryEntryInstitutionDataAdminInline, LinkAdminInline]
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "name",
                    "purpose",
                    "description",
                    "areas",
                    "tags",
                    "developers",
                    "published",
                ]
            },
        ),
        (
            _("OBDOBJE RABE"),
            {
                "fields": [
                    "time_in_use",
                    "time_in_use_date",
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
admin.site.register(RegistryEntryInstitutionData, RegistryEntryInstitutionDataAdmin)
admin.site.register(Link)
admin.site.register(GenericTag)
admin.site.register(AreaTag)
admin.site.register(InstitutionTag)
