# Generated by Django 5.1.1 on 2024-10-04 12:59

import django.db.models.deletion
import taggit.managers
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        (
            "taggit",
            "0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="RegistryEntry",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=100, verbose_name="Ime orodja")),
                (
                    "purpose",
                    models.CharField(max_length=255, verbose_name="Namen orodja"),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="Kakšne odločitve se sprejemajo, kaj dela ta algoritem",
                        verbose_name="Opis",
                    ),
                ),
                (
                    "time_in_use",
                    models.CharField(
                        blank=True, max_length=30, verbose_name="Obdobje rabe"
                    ),
                ),
                (
                    "institution",
                    models.CharField(
                        blank=True, max_length=255, verbose_name="Institucija"
                    ),
                ),
                ("area", models.TextField(blank=True, verbose_name="Področje rabe")),
                (
                    "developers",
                    models.CharField(
                        blank=True, max_length=255, verbose_name="Razvijalci"
                    ),
                ),
                (
                    "cost",
                    models.CharField(blank=True, max_length=50, verbose_name="Cena"),
                ),
                (
                    "cost_comment",
                    models.TextField(blank=True, verbose_name="Komentarji o ceni"),
                ),
                (
                    "data_sources",
                    models.TextField(
                        blank=True, verbose_name="Viri podatkov, ki jih uporablja"
                    ),
                ),
                (
                    "license_duration",
                    models.CharField(
                        blank=True,
                        max_length=50,
                        verbose_name="Trajanje licence (če kupljeno)",
                    ),
                ),
                (
                    "human_rights_analysis_done",
                    models.BooleanField(
                        default=False,
                        verbose_name="Analiza učinka na človekove pravice opravljena",
                    ),
                ),
                (
                    "human_rights_analysis_comments",
                    models.TextField(
                        blank=True,
                        verbose_name="Komentarji analize učinka na človekove pravice",
                    ),
                ),
                (
                    "personal_data_analysis_done",
                    models.BooleanField(
                        default=False,
                        verbose_name="Analiza učinka na osebne podatke opravljena",
                    ),
                ),
                (
                    "personal_data_analysis_comments",
                    models.TextField(
                        blank=True,
                        verbose_name="Komentarji analize učinka na osebne podatke",
                    ),
                ),
                (
                    "comments",
                    models.TextField(
                        blank=True,
                        help_text="Interno",
                        verbose_name="Dodatni komentarji",
                    ),
                ),
                (
                    "tags",
                    taggit.managers.TaggableManager(
                        help_text="Ločene z vejico",
                        through="taggit.TaggedItem",
                        to="taggit.Tag",
                        verbose_name="Oznake",
                    ),
                ),
            ],
            options={
                "verbose_name": "Vnos v register",
                "verbose_name_plural": "Vnosi v register",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Link",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("url", models.URLField(verbose_name="Povezava")),
                (
                    "description",
                    models.CharField(max_length=255, verbose_name="Opis povezave"),
                ),
                (
                    "registy_entry",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="links",
                        to="home.registryentry",
                    ),
                ),
            ],
            options={
                "verbose_name": "Povezava",
                "verbose_name_plural": "Povezave",
            },
        ),
    ]
