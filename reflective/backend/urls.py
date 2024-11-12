from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('', views.home_view, name='home'),
    path('about/', views.about, name='about'),
    path('create-survey/', views.create_survey, name='create_survey'),
    path('profile/', views.profile_view, name='profile'),
    path('survey-success/', views.survey_success,
         name='survey_success'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
