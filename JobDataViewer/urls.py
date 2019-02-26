"""JobDataViewer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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

from django.contrib import admin
from django.conf.urls import url, include
from django.views.generic import TemplateView
from viewer import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='home'),
    url(r'^chart/', views.data_viewer, name='chart'),
    url(r'^get_trend_by_word/$', views.get_trend_by_word, name='get_trend_by_word'),
    url(r'^lang_ranking/$', views.language_trend, name='lang-ranking'),
    url(r'^blog/', include('blog.urls')),
    # Using app_name with include is deprecated in Django 1.9
    # and does not work in Django 2.0. Set app_name in account/urls.py instead
    # url(r'^account/', include('account.urls', namespace='account', app_name='account')),
    url(r'^account/', include('account.urls')),
    url(r'^article/', include('article.urls')),
    url(r'home/', TemplateView.as_view(template_name="index.html"), name="index"),
    url(r'^image/', include('image.urls')),
]
