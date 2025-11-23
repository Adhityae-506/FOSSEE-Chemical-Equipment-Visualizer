from django.urls import path
from .views import dataset_upload, LatestSummaryView, HistoryView, LatestReportView
from .auth_views import LoginView

urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='api_login'),
    path('datasets/upload/', dataset_upload, name='dataset-upload'),
    path('datasets/latest/', LatestSummaryView.as_view(), name='dataset-latest'),
    path('datasets/history/', HistoryView.as_view(), name='dataset-history'),
    path('datasets/latest/report/', LatestReportView.as_view(), name='dataset-latest-report'),
]
