from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.login_view),
    path('signup/',views.signup),
    path('logout/',views.logout_view),
    path('checklogin/',views.check_user_login),
    path('myshares/', views.share_list_create, name='share-list-create'),
    path('shares/<int:pk>/', views.share_detail, name='share-detail'),

]