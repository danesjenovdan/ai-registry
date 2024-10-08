from django.db import models
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager


class Timestamped(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Link(models.Model):
    url = models.URLField(verbose_name=_("Povezava"))
    description = models.CharField(max_length=255, verbose_name=_("Opis povezave"))
    registy_entry = models.ForeignKey(
        "RegistryEntry",
        on_delete=models.CASCADE,
        related_name="links",
    )

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = _("Povezava")
        verbose_name_plural = _("Povezave")


class RegistryEntry(Timestamped):
    name = models.CharField(max_length=100, verbose_name=_("Ime orodja"))
    purpose = models.CharField(max_length=255, verbose_name=_("Namen orodja"))
    description = models.TextField(
        blank=True,
        verbose_name=_("Opis"),
        help_text=_("Kakšne odločitve se sprejemajo, kaj dela ta algoritem"),
    )
    # links = Related
    #   Povezava do pridobljenih materialov / viri
    time_in_use = models.CharField(
        max_length=30,
        blank=True,
        verbose_name=_("Obdobje rabe"),
    )
    institution = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Institucija"),
    )
    area = models.TextField(
        blank=True,
        verbose_name=_("Področje rabe"),
    )
    tags = TaggableManager(
        blank=True,
        verbose_name=_("Oznake"),
        help_text=_("Ločene z vejico"),
    )
    developers = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Razvijalci"),
    )
    cost = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_("Cena"),
    )
    cost_comment = models.TextField(
        blank=True,
        verbose_name=_("Komentarji o ceni"),
    )
    data_sources = models.TextField(
        blank=True,
        verbose_name=_("Viri podatkov, ki jih uporablja"),
    )
    license_duration = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_("Trajanje licence (če kupljeno)"),
    )
    human_rights_analysis_done = models.BooleanField(
        default=False,
        verbose_name=_("Analiza učinka na človekove pravice opravljena"),
    )
    human_rights_analysis_comments = models.TextField(
        blank=True,
        verbose_name=_("Komentarji analize učinka na človekove pravice"),
    )
    personal_data_analysis_done = models.BooleanField(
        default=False,
        verbose_name=_("Analiza učinka na osebne podatke opravljena"),
    )
    personal_data_analysis_comments = models.TextField(
        blank=True,
        verbose_name=_("Komentarji analize učinka na osebne podatke"),
    )
    comments = models.TextField(
        blank=True,
        verbose_name=_("Dodatni komentarji"),
        help_text=_("Interno"),
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Vnos v register")
        verbose_name_plural = _("Vnosi v register")
        ordering = ["-created_at"]
