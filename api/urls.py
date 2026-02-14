from django.urls import path
from . import views

urlpatterns = [
    path('health', views.health_check, name='health_check'),
    path('', views.api_root, name='api_root'),
    path('resumes', views.create_resume_api, name='create_resume'),
    path('resumes/', views.list_resumes, name='list_resumes'),
    path('resumes/<str:resume_id>', views.get_resume, name='get_resume'),
    path('resumes/<str:resume_id>/', views.get_resume, name='get_resume_alt'),
    path('resumes/<str:resume_id>/delete', views.delete_resume_api, name='delete_resume'),
]
