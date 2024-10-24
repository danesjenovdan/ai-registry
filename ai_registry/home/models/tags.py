from django.db import models
from django.utils.translation import gettext_lazy as _
from taggit.models import GenericTaggedItemBase, TagBase


def custom_tag_string_parser(tag_string):
    return [t.strip(' "') for t in tag_string.split(";") if t.strip(' "')]


def custom_tag_string_joiner(tags):
    return "; ".join(t.name for t in tags)


class GenericTag(TagBase):
    class Meta:
        verbose_name = _("Oznaka")
        verbose_name_plural = _("Oznake")


class InstitutionTag(TagBase):
    class Meta:
        verbose_name = _("Institucija")
        verbose_name_plural = _("Institucije")


class AreaTag(TagBase):
    class Meta:
        verbose_name = _("Področje")
        verbose_name_plural = _("Področja")


class TaggedGeneric(GenericTaggedItemBase):
    tag = models.ForeignKey(
        GenericTag,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items",
    )

    class Meta:
        verbose_name = _("Oznaka")
        verbose_name_plural = _("Oznake")


class TaggedInstitution(GenericTaggedItemBase):
    tag = models.ForeignKey(
        InstitutionTag,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items",
    )

    class Meta:
        verbose_name = _("Oznaka institucije")
        verbose_name_plural = _("Oznake institucij")


class TaggedArea(GenericTaggedItemBase):
    tag = models.ForeignKey(
        AreaTag,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items",
    )

    class Meta:
        verbose_name = _("Oznaka področja")
        verbose_name_plural = _("Oznake področij")
