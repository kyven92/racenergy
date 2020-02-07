"""racenery_IOT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include,path
from rest_framework.authtoken.views import obtain_auth_token  # <-- Here
from racIOT import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-token-auth/', obtain_auth_token,name='api_token_auth'),
    path('hello/',views.helloView.as_view(),name='hello'),
    path('upload-rps-data/',views.uploadRPSData.as_view()),
    path('get-latest-entry/',views.getLatestEmtry.as_view()),
    
    path('accounts/login/',auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    # path('accounts/logout/',auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('accounts/logout/',auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('', views.HomePageView.as_view(), name='home'),

    path('api/chart/data/', views.no_of_students.as_view()),
    path('api/chart/gender_percentage/', views.genderPercentage.as_view()),
    path('api/chart/ailments/', views.genderAilments.as_view())

]
