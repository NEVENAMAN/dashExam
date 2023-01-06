from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('register',views.register),
    path('login',views.login),
    path('user_page',views.user_page),
    path('add_pypiy_by_user',views.add_pypiy_by_user),
    path('edit_pypie_page/<int:pypieId>',views.edit_pypie_page),
    path('edit_pypie_process/<int:pypieId>',views.edit_pypie_process),
    path('del_pypie_data/<int:pypieId>',views.del_pypie_data),
    path('pypies',views.pypies),
    path('show_pypie/<int:pypieId>',views.show_pypie),
    path('log_out',views.log_out),
    path('vote',views.vote),
    path('del_vote',views.del_vote),
]