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
from JobDataViewer import settings
from django.conf.urls import url, include
from viewer import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/', views.data_viewer, name='home'),
    url(r'^chart/', views.data_viewer, name='chart'),
    url(r'^get_trend_by_word/$', views.get_trend_by_word, name='get_trend_by_word'),
    url(r'^lang_ranking/$', views.language_trend, name='lang-ranking'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns