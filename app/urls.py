
from django.urls import path
from app import views
urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('contact/', views.ContactPage.as_view(), name='contact'),
    path('about/', views.AboutPage.as_view(), name='about'),
    path('categories/', views.CategoryView.as_view(), name='category'),
    path('categories/<int:category_id>/products/', views.ProductListByCategoryView.as_view(), name='products_by_category'),

    ############### DETAIL PAGE #################
    path('product/<slug:slug>/',views.ProductDetailView.as_view(), name='product_detail' )
]
