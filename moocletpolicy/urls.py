"""moocletpolicy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from moocletpolicy import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^getmoocletversion/', views.get_mooclet_version, name="get mooclet version"),
    url(r'^testupdatevars/', views.test_update_vars, name="test updating vars"),
    url(r'^testcreateweightset/', views.test_create_weightset, name="test creating a set of weights"),
    url(r'^getversionwithoutreplacement/', views.get_mooclet_version_without_replacement_policy, name="test getting without replacement"),
]
