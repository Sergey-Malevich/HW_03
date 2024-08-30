from django.urls import path
from .views import IndexView, upgrade_me
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('upgrade/', upgrade_me, name = 'upgrade'),
    path('', IndexView.as_view(), name='user_cab'),
    path('login/',
         LoginView.as_view(template_name='users/login.html'),
         name='login'),
    path('logout/',
         LogoutView.as_view( http_method_names=["post", "get", "options"],template_name='users/logout.html'),
         name='logout'),
]
