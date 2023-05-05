"""Spam_Detection URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static


from Spam_Detection import settings
from Client import views as user_view
from Research import views as admin_view

urlpatterns = [
    url('admin/', admin.site.urls),
    url('^$', user_view.user_login, name="user_login"),

    url(r'^user_register/$',user_view.user_register, name="user_register"),
    url(r'^user_mydetails/$',user_view.user_mydetails, name="user_mydetails"),
    url(r'^user_updatedetails/$',user_view.user_updatedetails, name="user_updatedetails"),
    url(r'^tweet/$',user_view.tweet, name="tweet"),
    url(r'^tweetview/$',user_view.tweetview, name="tweetview"),
    url(r'^feedback/$',user_view.feedback, name="feedback"),

    url(r'^admin_login/$', admin_view.admin_login, name="admin_login"),
    url(r'admin_viewpage/$',admin_view.admin_viewpage,name="admin_viewpage"),
    url(r'classification/$',admin_view.classification,name="classification"),
    path(r'classification/block/<int:id>/', admin_view.block, name='block'),
    url(r'admin_viewfeedback/$',admin_view.admin_viewfeedback,name="admin_viewfeedback"),
    url(r'admin_viewtrending/$',admin_view.admin_viewtrending,name="admin_viewtrending"),
    url(r'^viewtreandingtopics/(?P<chart_type>\w+)/$', admin_view.viewtreandingtopics,name="viewtreandingtopics"),
    url(r'^negativefeedbacktivechart/(?P<chart_type>\w+)/$', admin_view.negativefeedbacktivechart,name="negativefeedbacktivechart"),


]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
