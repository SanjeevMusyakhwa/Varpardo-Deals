from urllib import request
from django.shortcuts import redirect, render,get_object_or_404
from django.views.generic import TemplateView, ListView, View
from app.models import *
from django.db.models import Count, Q
from .models import Category


######################## HOME VIEW ##################################
######################## HOME VIEW ##################################
######################## HOME VIEW ##################################
######################## HOME VIEW ##################################
######################## HOME VIEW ##################################


class HomePage(TemplateView):
  template_name = 'home.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['products'] = Product.objects.all().order_by('-id')

    return context


######################## CATEGORY VIEW ##################################
######################## CATEGORY VIEW ##################################
######################## CATEGORY VIEW ##################################
######################## CATEGORY VIEW ##################################
######################## CATEGORY VIEW ##################################


class CategoryView(TemplateView):
    template_name = 'categories.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        filter_available_products = self.request.GET.get('filter_available_products', False)

        category_id = self.kwargs.get("category_id")
        if category_id:
            # If category_id is provided, filter products by that category
            categories = Category.objects.annotate(
                available_products_count=Count('product', filter=Q(product__is_available=True))
            ).filter(available_products_count__gt=0).order_by('-available_products_count')

            # Pass only the selected category to the context
            selected_category = Category.objects.get(id=category_id)
            context['category'] = selected_category
            products = Product.objects.filter(category_id=category_id)
        else:
            # If no category is selected, show all categories and products
            categories = Category.objects.all()
            products = Product.objects.all()

        if filter_available_products:
            # Optionally filter products by availability
            products = products.filter(is_available=True)

        # Add categories and products to context
        context['categories'] = categories
        context['products'] = products

        return context
    

######################## PRODUCT LIST BY CATEGORY ##################################
######################## PRODUCT LIST BY CATEGORY ##################################
######################## PRODUCT LIST BY CATEGORY ##################################
######################## PRODUCT LIST BY CATEGORY ##################################
######################## PRODUCT LIST BY CATEGORY ##################################

class ProductListByCategoryView(ListView):
    model = Product
    template_name = 'categories.html'  # Use the same template to display products in a category
    context_object_name = 'products'
    paginate_by = 10  # Optional: add pagination

    def get_queryset(self):
        # Retrieve the category ID from the URL parameters
        category_id = self.kwargs.get('category_id')
        filter_available_products = self.request.GET.get('filter_available_products', False)

        # Filter products by category and optionally by availability
        queryset = Product.objects.filter(category_id=category_id)
        
        if filter_available_products:
            queryset = queryset.filter(is_available=True)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add the selected category to the context
        category_id = self.kwargs.get('category_id')
        context['category'] = Category.objects.get(id=category_id)
        
        # Always include the category list in the sidebar
        filter_available_products = self.request.GET.get('filter_available_products', False)
        if filter_available_products:
            categories = Category.objects.annotate(
                available_products_count=Count('product', filter=Q(product__is_available=True))
            ).filter(available_products_count__gt=0).order_by('-available_products_count')
        else:
            categories = Category.objects.all()
        
        context['categories'] = categories
        
        return context


######################## CONTACT VIEW ##################################
######################## CONTACT VIEW ##################################
######################## CONTACT VIEW ##################################
######################## CONTACT VIEW ##################################
######################## CONTACT VIEW ##################################


class ContactPage(TemplateView):
  template_name = 'contact.html'


######################## ABOUT VIEW ##################################
######################## ABOUT VIEW ##################################
######################## ABOUT VIEW ##################################
######################## ABOUT VIEW ##################################
######################## ABOUT VIEW ##################################


class AboutPage(TemplateView):
  template_name = 'about.html'


######################## PRODUCT DETAIL VIEW ##################################
######################## PRODUCT DETAIL VIEW ##################################
######################## PRODUCT DETAIL VIEW ##################################
######################## PRODUCT DETAIL VIEW ##################################
######################## PRODUCT DETAIL VIEW ##################################


class ProductDetailView(TemplateView):
   template_name = 'product_detail.html'


   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      slug = kwargs['slug']
      product = Product.objects.get(slug = slug)
      product.view_count += 1
      product.save()
      context['product'] = product
      return context
   

######################## ADD TO CART VIEW ##################################
######################## ADD TO CART VIEW ##################################
######################## ADD TO CART VIEW ##################################
######################## ADD TO CART VIEW ##################################
######################## ADD TO CART VIEW ##################################



class CartView(TemplateView):
    template_name = 'cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get('cart_id', None)
        
        # Retrieve the cart if it exists
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = None

        context["cart"] = cart
        return context
    
class AddToCartView(View):
    def get(self, request, product_id):
        # Get or create the cart ID in the session
        cart_id = request.session.get('cart_id', None)
        
        if cart_id:
            try:
                cart_obj = Cart.objects.get(id=cart_id)
            except Cart.DoesNotExist:
                # Create a new cart if the old one is missing
                cart_obj = Cart.objects.create(total=0)
                request.session['cart_id'] = cart_obj.id
        else:
            # No cart ID in session, create a new cart
            cart_obj = Cart.objects.create(total=0)
            request.session['cart_id'] = cart_obj.id

        # Get the product
        product_obj = get_object_or_404(Product, id=product_id)
        
        # Check if the product is already in the cart
        cart_product, created = CartProduct.objects.get_or_create(
            cart=cart_obj,
            product=product_obj,
            defaults={'rate': product_obj.selling_price, 'quantity': 0, 'subtotal': 0}
        )

        # Increase quantity if already in cart, otherwise set initial quantity to 1
        if not created:
            cart_product.quantity += 1
        else:
            cart_product.quantity = 1
        
        # Update subtotal and save cart product
        cart_product.subtotal = cart_product.quantity * cart_product.rate
        cart_product.save()

        # Update cart total and save
        cart_obj.total = sum(item.subtotal for item in cart_obj.cartproduct_set.all())
        cart_obj.save()

        # Redirect to the cart page or wherever you want
        return redirect('cart_view')


    

class ManageCart(View):
    def get(self,request,*args, **kwargs):
        print("This is manage cart Section")
        cart_id = self.kwargs['cart_id']
        action = request.GET.get('action')
        print(cart_id,action)
        return redirect('cart')
