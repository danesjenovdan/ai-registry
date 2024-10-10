from django.core.paginator import Paginator
from django.views.generic import TemplateView

from .models import RegistryEntry


class HomeView(TemplateView):
    template_name = "home/home_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        entries = RegistryEntry.objects.all()
        paginator = Paginator(entries, 10)
        page_query = self.request.GET.get("page", 1)
        page_obj = paginator.get_page(page_query)
        paginator.elided_page_range = paginator.get_elided_page_range(
            number=page_obj.number,
            on_each_side=3,
            on_ends=0,
        )

        context["entries"] = page_obj

        return context
