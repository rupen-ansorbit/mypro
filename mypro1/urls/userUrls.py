from django.urls import path
from mypro1.views import userViews

userUrlpatterns = [
   # path('create', userViews.create_user, name='create_user'),
   path('register', userViews.register_user, name='register_user'),
   path ('login', userViews.login_user, name='login_user'),
   path('user', userViews.get_user_data, name='get_user_data'),
   # path('', userViews.get_user, name='get_user'),    
   path('delete/<str:id>', userViews.delete_user, name='delete_user'),
   path('update/<str:id>', userViews.update_user, name='update_user'),
   # path('<str:id>', userViews.get_user_by_id, name='get_user_by_id'),
] 