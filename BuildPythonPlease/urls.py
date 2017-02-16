"""BuildPythonPlease URL Configuration

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
from django.conf.urls import url
from django.contrib.auth import views as auth_views

from BuildPythonPleaseGUI import views as BPP_views
from BuildPythonPleaseGUI import forms as BPP_forms

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #no authentication required
    url(r'^$', BPP_views.home),
    url(r'^login/', auth_views.login, {"template_name": "BuildPythonPleaseGUI/login.html",
                                       "authentication_form": BPP_forms.LoginForm,
                                       },name="login"), 
    url(r"^logout/", auth_views.logout, {"next_page": "/login"}),
    url(r'^register/', BPP_views.register),
    url(r'^terms_and_conditions/', BPP_views.terms_and_conditions),
    url(r'^success/', BPP_views.success),
    url(r'^about_us/', BPP_views.about_us),

    #authentication required
    url(r'^projects/', BPP_views.projects),
    url(r'^project/(?P<id>.*)/$', BPP_views.project),
    url(r'^create_project/', BPP_views.create_project),

    #admins only
    url(r'^all_users/', BPP_views.all_users),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
