# urls.py

from django.urls import path
from home import views
from . import views

urlpatterns = [
     path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.login_user, name='login'),  # Added login path
    path('register/', views.register_user, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('add_advertising/', views.add_advertising, name='add_advertising'),
    path('view_advertisements/', views.view_advertisements, name='view_advertisements'),
    path('delete/<int:advertisementid>/', views.delete_advertisement, name="delete_advertisement"), 
    path('edit/<int:advertisementid>/', views.edit_advertisements, name="edit_advertisement"),
    path('services/', views.user_services, name="services"),
    path('add_to_list/<int:advertisementid>/', views.add_to_list, name="add_to_list"),
    path('show_list/', views.show_list, name="show_list"),
    path('delete_list/<int:fadvertisementid>/', views.delete_list, name='delete_list'),
    path('category/<category_value>/', views.filter_by_category, name="category"),
    path('price-range/', views.price_range, name="search_by_price_range"),
    path('admin_order_history/', views.admin_order_history, name='admin_order_history'),
    path('make_payment/', views.make_payment, name='make_payment'),
    path('order_history/', views.order_history, name='order_history'),
    path('products/order/<payment_id>/<amount>', views.order),
    path('forgotpassword/', views.forgot_password, name="forgot_password"),
    path('forgotpassword/update/<uname>', views.passotp, name="passotp"),
    path('search_by_name/', views.searchByName, name='search_by_name'),
  
     

]
