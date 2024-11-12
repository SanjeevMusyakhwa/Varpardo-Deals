
from django.urls import path
from app import views
app_name = 'app'
urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('categories/', views.CategoryView.as_view(), name='category'),
    path('categories/<int:category_id>/products/', views.ProductListByCategoryView.as_view(), name='products_by_category'),

    ############### DETAIL PAGE #################
    path('product/<slug:slug>/',views.ProductDetailView.as_view(), name='product_detail' ),

    ############## ADD TO CART  ################
    path('cart/', views.CartView.as_view(), name='cart_view'),
    path('add_to_cart/<int:product_id>/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('manage_cart/<int:cp_id>/', views.ManageCart.as_view(), name='manage_cart'),
    path('empty_cart/', views.EmptyCart.as_view(), name='empty_cart'),
    path('checkout/', views.Checkout.as_view(), name='checkout'),
    path('search/', views.Search.as_view(), name='search'),

     ############## REGISTERATION ######################
     path('register/', views.CustomerRegister.as_view(), name='customerregistration'),
     path('logout/', views.CustomerLogout.as_view(), name='customerlogout'),
     path('login/', views.CustomerLogin.as_view(), name='customerlogin'),

     path('profile/', views.CustomerProfile.as_view(), name='customerprofile'),
     path('profile/order-<int:pk>/', views.CustomerOrderDetail.as_view(), name='customerorderdetail'),


     ################################################## ADMIN PANEL ######################################################
     path('adminlogin/', views.AdminLogin.as_view(), name='adminlogin'),
     path('admin_home/', views.AdminHomePage.as_view(), name='adminhome'),
     path('adminorder_detail/<int:pk>/', views.AdminOrderDetail.as_view(), name='adminorderdetail'),
     path('adminallorder/', views.AdminAllOrder.as_view(), name='adminallorder'),
     path('adminorder-<int:pk>-change/', views.AdminOrderStatusChange.as_view(), name='adminorderchange'),
     path('adminlogout/', views.AdminLogout.as_view(), name='adminlogout'),


]