"""ctfspace URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import RedirectView

from challenges.views import ranking, ChallengeListView, challenge_detail_view
from notice.views import NoticeListView, NoticeDetailView
from .views import dashboard

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^scoreboard/', ranking, name='ranking'),
    url(r'^challenges/$', ChallengeListView.as_view(), name='challenges'),
    url(r'^challenges/(?P<pk>\d+)/', challenge_detail_view, name='challenge'),
    url(r'^notice/$', NoticeListView.as_view(), name='notices'),
    url(r'^notice/(?P<pk>\d+)/', NoticeDetailView.as_view(), name='notice'),
    url(r'^dashboard/$', dashboard, name='dashboard'),
    url(r'^$', RedirectView.as_view(url='/dashboard'))
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)