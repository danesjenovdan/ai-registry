from django.db import models
from django.utils.translation import gettext_lazy as _
from taggit.models import GenericTaggedItemBase, TagBase


class GenericTag(TagBase):
    class Meta:
        verbose_name = _("Oznaka")
        verbose_name_plural = _("Oznake")


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


class TaggedArea(GenericTaggedItemBase):
    tag = models.ForeignKey(
        AreaTag,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items",
    )

    class Meta:
        verbose_name = _("Oznaka področja")
        verbose_name_plural = _("Oznake področij")
