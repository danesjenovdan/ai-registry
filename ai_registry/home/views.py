from django.core.paginator import Paginator
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

from .models.registry_entry import RegistryEntry
from .models.tags import AreaTag, GenericTag, InstitutionTag

SORT_OPTIONS = [
    ("time_in_use_date", _("obdobju rabe")),
    ("updated_at", _("zadnjem vnosu")),
]
SORT_KEYS = [key for key, _ in SORT_OPTIONS]
SORT_DEFAULT = "updated_at"


def _get_tags(request, Model, key, entries):
    objects = list(
        Model.objects.filter(registryentry__in=entries)
        .distinct()
        .values_list("slug", "name")
    )
    object_dict = {slug: name for slug, name in objects}

    query_param = request.GET.get(key, "")
    try:
        selected_tuple = (query_param, object_dict[query_param])
    except KeyError:
        selected_tuple = None

    return objects, selected_tuple


class HomeView(TemplateView):
    template_name = "home/home_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        entries = RegistryEntry.objects.all()
        all_entries_count = entries.count()

        areas, selected_area = _get_tags(self.request, AreaTag, "area", entries)
        tags, selected_tag = _get_tags(self.request, GenericTag, "tag", entries)
        institutions, selected_institution = _get_tags(
            self.request, InstitutionTag, "institution", entries
        )

        if selected_area:
            entries = entries.filter(areas__slug=selected_area[0])
        if selected_tag:
            entries = entries.filter(tags__slug=selected_tag[0])
        if selected_institution:
            entries = entries.filter(institutions__slug=selected_institution[0])

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
            "selected_area": selected_area,
            "selected_tag": selected_tag,
            "selected_institution": selected_institution,
        }
        context["search"] = search

        return context
