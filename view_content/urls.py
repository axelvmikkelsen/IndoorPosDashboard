from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    #path('dashboard', views.view_dash, name="dashboard"),
    #path('#', views.connect_to, name="connect_to"),
    path('1', views.disconnect, name="disconnect"),
    path('', views.home, name="home"),
    path('save', views.save_session_name),
    path('connection', views.establish_connection),
    path('disconnection', views.teardown_connection),
    path('collect_tags', views.collect_tags),
    path('floor', views.floor_params),
    path('session', views.session)
]
