from django.urls import path,include
from .views import *

app_name = 'assignment'

urlpatterns = [
    path('registration', user_Registration, name="registration"),
    path('user_login', user_Login, name="user_login"),
    path('user_logout', user_logout, name="user_logout"),
    path('request', Request_view.as_view(), name="request"),
    path('request/create/', create_request, name="create"),
    path('request/update/<int:pk>', update_request, name="update"),
    path('request/detail/<int:pk>', Detail_request.as_view(), name="detail"),
    # path('request/delete/<int:pk>', delete_request, name="delete"),
    path('forgetpassword', forgetpassword, name="forgetpassword"),
    path('forgetPasswordPage', forgetPasswordPage, name="forgetPasswordPage"),
]
