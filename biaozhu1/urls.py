"""biaozhu1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from polls import views as polls_views
#from django.urls import path
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', polls_views.login, name='login'),
    url(r'^insert_choice/$', polls_views.insert_record, name='insert-record'),
    url(r'^update_choice/$', polls_views.update_record, name='update-record'),
    url(r'^admin/index/', polls_views.get_info, name='get-info'),
    url(r'^admin/polls/timeCount/', polls_views.timeCount, name='timeCount'),
    url(r'^admin/polls/recordAccount/', polls_views.recordAccount, name='recordAccount'),
    url(r'^admin/polls/randomManage/', polls_views.randomManage, name='randomManage'),
    url(r'^admin/', admin.site.urls),
    # path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
