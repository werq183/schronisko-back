"""
URL configuration for schronisko project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import include, path
from rest_framework import routers
from django.contrib import admin
from app import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/login', views.login),
    path('api/register', views.register),
    path('api/logout', views.logout),
    path('api/test_token', views.test_token),
    path('api/profile', views.profile),
    path('api/ogloszenia', views.list_ogloszenia_with_details),
    path('api/ogloszenia/<int:pk>', views.get_ogloszenie_by_id),
    path('api/rezerwacja', views.reserve)
    # path('kot/<int:pk>', UpdateKot.as_view(), name='update_kot')
]