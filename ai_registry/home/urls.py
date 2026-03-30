from django.urls import path

from .views import CSVExportView, HomeView, RobotsTxtView

urlpatterns = [
    path("", HomeView.as_view(), name="home_view"),
    path("robots.txt", RobotsTxtView.as_view(), name="robots_txt"),
    path("export/data.csv", CSVExportView.as_view(), name="csv_export"),
]
