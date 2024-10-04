from django.views.generic import TemplateView

from .models import RegistryEntry


class HomeView(TemplateView):
    template_name = "home/home_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["entries"] = RegistryEntry.objects.all()
        return context
