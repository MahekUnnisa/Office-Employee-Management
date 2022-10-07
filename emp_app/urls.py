from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('manage',views.manage, name="manage"),
    path("register", views.handleRegister, name="handlerRegister"),
    path("login",views.handleLogin, name='handleLogin' ),
    path("logout",views.handleLogout, name='handleLogout' ),
    path('viewallemployees', views.viewallemployees, name='viewallemployees'),
    path('addanemployee',views.addanemployee, name='addanemployee'),
    path('filterallemployees',views.filterallemployees, name='filterallemployees'),
    path('removeanemployee',views.removeanemployee, name='removeanemployee'),
    path('removeanemployee/<int:emp_id>',views.removeanemployee, name='removeanemployee'),

]
