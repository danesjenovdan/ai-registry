from django.db import models
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager

from .base import Timestamped
from .tags import custom_tag_string_joiner


class Link(models.Model):
    # related registry entry
    registry_entry = models.ForeignKey(
        "RegistryEntry",
        on_delete=models.CASCADE,
        related_name="links",
    )
    # general fields
    description = models.CharField(
        max_length=255,
        verbose_name=_("Opis povezave"),
    )
    url = models.URLField(
        null=True,
        blank=True,
        verbose_name=_("Povezava"),
    )
    file = models.FileField(
        null=True,
        blank=True,
        verbose_name=_("Datoteka"),
    )

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = _("Povezava")
        verbose_name_plural = _("Povezave")


class RegistryEntryInstitutionData(Timestamped):
    # related registry entry
    registry_entry = models.ForeignKey(
        "RegistryEntry",
        on_delete=models.CASCADE,
        related_name="registryentryinstitutiondata",
    )
    # general fields
    institution = TaggableManager(
        through="home.TaggedInstitution",
        blank=True,
        related_name="registryentryinstitutiondata_institution",
        verbose_name=_("Institucija"),
        help_text="",
    )
    # cost
    cost = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_("Cena"),
    )
    cost_comment = models.TextField(
        blank=True,
        verbose_name=_("Komentarji o ceni"),
    )
    # license
    license_duration = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_("Trajanje licence (če kupljeno)"),
    )
    license_duration_comment = models.TextField(
        blank=True,
        verbose_name=_("Komentarji o trajanju licence"),
    )
    # analyses
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
    # public procurements
    public_procurement = models.BooleanField(
        default=False,
        verbose_name=_("Javno naročilo"),
        help_text=_("Ali je bil vnos predmet javnega naročila?"),
    )
    public_procurement_number = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name=_("Številka objave na PJN"),
        help_text=_(
            "Številka javnega naročila na portalu javnih naročil (PJN), če je predmet javnega naročila"
        ),
    )
    public_procurement_number_eu = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name=_("Številka objave na TED"),
        help_text=_(
            "Številka javnega naročila na portalu TED (tenders electronic daily), če je predmet javnega naročila"
        ),
    )
    public_procurement_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Datum objave javnega naročila"),
        help_text=_("Datum objave javnega naročila, če je predmet javnega naročila"),
    )
    contracting_institution = TaggableManager(
        through="home.TaggedContractingInstitution",
        blank=True,
        related_name="registryentryinstitutiondata_contracting_institution",
        verbose_name=_("Naročnik"),
        help_text="",
    )

    def __str__(self):
        institution = custom_tag_string_joiner(self.institution.all())
        return f"{self.registry_entry} - {institution}"

    class Meta:
        verbose_name = _("Podatki institucije pri vnosu")
        verbose_name_plural = _("Podatki institucij pri vnosih")


class RegistryEntry(Timestamped):
    name = models.CharField(max_length=100, verbose_name=_("Ime orodja"))
    purpose = models.CharField(max_length=255, verbose_name=_("Namen orodja"))
    description = models.TextField(
        blank=True,
        verbose_name=_("Opis"),
        help_text=_("Kakšne odločitve se sprejemajo, kaj dela ta algoritem"),
    )
    areas = TaggableManager(
        through="home.TaggedArea",
        blank=True,
        verbose_name=_("Področja"),
        help_text=_("Ločena s podpičjem"),
    )
    tags = TaggableManager(
        through="home.TaggedGeneric",
        blank=True,
        verbose_name=_("Oznake"),
        help_text=_("Ločene s podpičjem"),
    )
    developers = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Razvijalci"),
    )
    published = models.BooleanField(
        default=True,
        verbose_name=_("Objavljeno"),
        help_text=_("Ali je vnos v register objavljen?"),
    )
    # time in use
    time_in_use = models.CharField(
        max_length=30,
        blank=True,
        verbose_name=_("Obdobje rabe (uporabljeno za prikaz)"),
    )
    time_in_use_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Obdobje rabe (uporabljeno za razvrščanje)"),
    )
    # internal
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
