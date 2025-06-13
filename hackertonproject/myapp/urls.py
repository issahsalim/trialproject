from django.urls import path 
from .import views 
from django.contrib.auth import views as auth_views 

urlpatterns=[ 
    path('',views.index,name='home'),
    path('signup',views.registerView,name='signup'),
    path('login',views.loginView,name='login'), 
    path('ai',views.chatbot,name='ai'), 
    # path('campusmap',views.campusMap,name='campusmap'), 
    path('api/search/', views.search_place, name='search_place'),
    path('api/support/', views.get_support_members, name='get_support'),
    path('map/', views.map_view, name='campusmap'),
    path('api/team-members/', views.team_members_api, name='team_members_api'),
    path('logout', views.logoutView, name='logout'),
    
     # RESETTING PASSWORD PATHS
     path('password_reset/',views.CustomPasswordResetView.as_view(
         template_name='reset_password.html',
         email_template_name="email_reset_password.html", 
         html_email_template_name="email_reset_password.html",
     ),name='password_reset'),  
     
     
     path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(
         template_name="reset_password_done.html",
         
     ),name="password_reset_done"),
     
     path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(
         template_name="reset_password_confirm.html"
     ),name="password_reset_confirm"),
     
     path('reset/done/',auth_views.PasswordResetCompleteView.as_view(
          template_name="reset_password_complete.html"  
     ),name='password_reset_complete'),

]


