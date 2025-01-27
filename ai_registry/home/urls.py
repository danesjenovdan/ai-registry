from django.urls import path

from .views import CSVExportView, HomeView

urlpatterns = [
    path("", HomeView.as_view(), name="home_view"),
    path("export/data.csv", CSVExportView.as_view(), name="csv_export"),
]
