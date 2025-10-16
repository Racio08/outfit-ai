from django.urls import path
from . import views

app_name = 'outfits'

urlpatterns = [
    path('', views.home, name='home'),
    path('process/', views.process_image, name='process_image'),
    path('statistics/', views.get_processing_statistics, name='statistics'),
    path('download-report/', views.download_statistics_report, name='download_report'),
    path('3d-visualization/', views.get_3d_visualization, name='3d_visualization'),
]