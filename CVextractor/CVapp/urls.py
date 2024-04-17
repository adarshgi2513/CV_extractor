from django.urls import path
from . import views  
from.views import upload_cv,download_cv_data_as_excel,success

urlpatterns = [
    path('', views.upload_cv, name='index'),
    path('success/',views.success, name='success'),
    path('download/', views.download_cv_data_as_excel, name='download'),
    # Add more URL patterns here as needed
]