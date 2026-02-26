import csv

from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView, View

from .models.registry_entry import RegistryEntry, RegistryEntryInstitutionData
from .models.tags import AreaTag, GenericTag, InstitutionTag

SORT_OPTIONS = [
    ("time_in_use_date", _("obdobju rabe")),
    ("updated_at", _("zadnjem vnosu")),
]
SORT_KEYS = [key for key, _ in SORT_OPTIONS]
SORT_DEFAULT = "updated_at"


def _get_tags_many(request, Model, key, entries, filter_key="registryentry__in"):
    objects = list(
        Model.objects.filter(**{filter_key: entries})
        .distinct()
        .values_list("slug", "name")
    )
    object_dict = {slug: name for slug, name in objects}

    selected_tuples = []
    query_param = request.GET.get(key, "")
    if query_params := query_param.split(","):
        for param in query_params:
            try:
                selected_tuples.append((param, object_dict[param]))
            except KeyError:
                pass

    return objects, selected_tuples


@method_decorator(cache_page(60 * 15), name="dispatch")  # Cache for 5 minutes
class HomeView(TemplateView):
    template_name = "home/home_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        entries = RegistryEntry.objects.filter(
            published=True,
        ).prefetch_related(
            "areas",
            "tags",
            "registryentryinstitutiondata",
        )
        all_entries_count = entries.count()

        inst_entries = RegistryEntryInstitutionData.objects.filter(
            registry_entry__in=entries,
            public_procurement=False,
        ).prefetch_related(
            "institution",
            "contracting_institution",
        )

        areas, selected_areas = _get_tags_many(self.request, AreaTag, "area", entries)
        tags, selected_tags = _get_tags_many(self.request, GenericTag, "tag", entries)
        institutions, selected_institutions = _get_tags_many(
            self.request,
            InstitutionTag,
            "institution",
            inst_entries,
            filter_key="registryentryinstitutiondata_institution__in",
        )

        if selected_areas:
            selected_area_slugs = [slug for slug, _ in selected_areas]
            entries = entries.filter(areas__slug__in=selected_area_slugs)
        if selected_tags:
            selected_tag_slugs = [slug for slug, _ in selected_tags]
            entries = entries.filter(tags__slug__in=selected_tag_slugs)
        if selected_institutions:
            selected_institution_slugs = [slug for slug, _ in selected_institutions]
            entries = entries.filter(
                registryentryinstitutiondata__institution__slug__in=selected_institution_slugs
            )

        sort_query = self.request.GET.get("sort", SORT_DEFAULT)
        if sort_query not in SORT_KEYS:
            sort_query = SORT_DEFAULT

        entries = entries.order_by(f"-{sort_query}", "id")

        search = self.request.GET.get("search", "")
        if search:
            entries = entries.filter(
                Q(name__icontains=search)
                | Q(purpose__icontains=search)
                | Q(description__icontains=search)
                | Q(developers__icontains=search)
            )

        entries = entries.distinct()

        page_query = self.request.GET.get("page", "1")
        paginator = Paginator(entries, 10)
        page_obj = paginator.get_page(page_query)
        paginator.elided_page_range = paginator.get_elided_page_range(
            number=page_obj.number,
            on_each_side=3,
            on_ends=0,
        )

        context["all_entries_count"] = all_entries_count
        context["entries"] = page_obj
        context["sort_query"] = sort_query
        context["sort_options"] = SORT_OPTIONS
        context["filters"] = {
            "areas": areas,
            "tags": tags,
            "institutions": institutions,
            "selected_areas": selected_areas,
            "selected_tags": selected_tags,
            "selected_institutions": selected_institutions,
        }
        context["search"] = search

        return context


class CSVExportView(View):
    def get(self, request, *args, **kwargs):
        file_name = _("izvoz-register-ui")
        latest_updated_entry = RegistryEntry.objects.order_by("-updated_at").first()
        if latest_updated_entry:
            file_name += (
                f"_{latest_updated_entry.updated_at.strftime('%Y-%m-%d_%H-%M-%S')}"
            )

        response = HttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": f'attachment; filename="{file_name}.csv"'},
        )

        writer = csv.writer(response)
        writer.writerow(
            [
                # general info
                _("Ime orodja"),
                _("Namen orodja"),
                _("Opis"),
                _("Področja"),
                _("Oznake"),
                _("Razvijalci"),
                # time in use
                _("Obdobje rabe"),
                # institution data
                _("Institucija"),
                _("Cena"),
                _("Komentarji o ceni"),
                _("Trajanje licence (če kupljeno)"),
                _("Komentarji o trajanju licence"),
                _("Analiza učinka na človekove pravice opravljena"),
                _("Komentarji analize učinka na človekove pravice"),
                _("Analiza učinka na osebne podatke opravljena"),
                _("Komentarji analize učinka na osebne podatke"),
                # related links
                _("Povezave"),
                # updated at
                _("Posodobljeno"),
            ]
        )

        entries = RegistryEntry.objects.prefetch_related(
            "links",
            "registryentryinstitutiondata",
        ).all()
        for entry in entries:
            links = [
                f"{link.description}: {link.url or link.file}"
                for link in entry.links.all()
            ]
            writer.writerow(
                [
                    # general info
                    entry.name,
                    entry.purpose,
                    entry.description,
                    "; ".join(str(a) for a in entry.areas.all()),
                    "; ".join(str(t) for t in entry.tags.all()),
                    entry.developers,
                    # time in use
                    entry.time_in_use,
                    # institution data
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    # related links
                    "; ".join(links),
                    # updated at
                    entry.updated_at.strftime("%Y-%m-%dT%H:%M:%S"),
                ]
            )
            inst_entries = entry.registryentryinstitutiondata.all()
            for inst_entry in inst_entries:
                writer.writerow(
                    [
                        # general info
                        "↳",
                        "",
                        "",
                        "",
                        "",
                        "",
                        # time in use
                        "",
                        # institution data
                        "; ".join(str(i) for i in inst_entry.institution.all()),
                        inst_entry.cost,
                        inst_entry.cost_comment,
                        inst_entry.license_duration,
                        inst_entry.license_duration_comment,
                        _("Da") if inst_entry.human_rights_analysis_done else _("Ne"),
                        inst_entry.human_rights_analysis_comments,
                        _("Da") if inst_entry.personal_data_analysis_done else _("Ne"),
                        inst_entry.personal_data_analysis_comments,
                        # related links
                        "",
                        # updated at
                        "",
                    ]
                )

        return response
