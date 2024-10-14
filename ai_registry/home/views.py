from django.core.paginator import Paginator
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

from .models import RegistryEntry

SORT_OPTIONS = [
    ("time_in_use", _("obdobju rabe")),
    ("updated_at", _("zadnjem vnosu")),
]
SORT_KEYS = [key for key, _ in SORT_OPTIONS]
SORT_DEFAULT = "time_in_use"


class HomeView(TemplateView):
    template_name = "home/home_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        page_query = self.request.GET.get("page", "1")
        sort_query = self.request.GET.get("sort", SORT_DEFAULT)
        if sort_query not in SORT_KEYS:
            sort_query = SORT_DEFAULT

        entries = RegistryEntry.objects.all().order_by(f"-{sort_query}", "id")
        paginator = Paginator(entries, 10)
        page_obj = paginator.get_page(page_query)
        paginator.elided_page_range = paginator.get_elided_page_range(
            number=page_obj.number,
            on_each_side=3,
            on_ends=0,
        )

        context["entries"] = page_obj
        context["sort_query"] = sort_query
        context["sort_options"] = SORT_OPTIONS

        return context
