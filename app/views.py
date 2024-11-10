
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import TemplateView, ListView, View, CreateView
from app.models import *
from django.db.models import Count, Q
from .models import Category
from django.contrib import messages
from app.forms import CheckoutForm
from django.urls import reverse_lazy



######################## HOME VIEW ##################################
######################## HOME VIEW ##################################
######################## HOME VIEW ##################################
######################## HOME VIEW ##################################
######################## HOME VIEW ##################################


class HomePage(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.all().order_by("-id")

        return context


######################## CATEGORY VIEW ##################################
######################## CATEGORY VIEW ##################################
######################## CATEGORY VIEW ##################################
######################## CATEGORY VIEW ##################################
######################## CATEGORY VIEW ##################################


class CategoryView(TemplateView):
    template_name = "categories.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        filter_available_products = self.request.GET.get(
            "filter_available_products", False
        )

        category_id = self.kwargs.get("category_id")
        if category_id:
            # If category_id is provided, filter products by that category
            categories = (
                Category.objects.annotate(
                    available_products_count=Count(
                        "product", filter=Q(product__is_available=True)
                    )
                )
                .filter(available_products_count__gt=0)
                .order_by("-available_products_count")
            )

            # Pass only the selected category to the context
            selected_category = Category.objects.get(id=category_id)
            context["category"] = selected_category
            products = Product.objects.filter(category_id=category_id)
        else:
            # If no category is selected, show all categories and products
            categories = Category.objects.all()
            products = Product.objects.all()

        if filter_available_products:
            # Optionally filter products by availability
            products = products.filter(is_available=True)

        # Add categories and products to context
        context["categories"] = categories
        context["products"] = products

        return context


######################## PRODUCT LIST BY CATEGORY ##################################
######################## PRODUCT LIST BY CATEGORY ##################################
######################## PRODUCT LIST BY CATEGORY ##################################
######################## PRODUCT LIST BY CATEGORY ##################################
######################## PRODUCT LIST BY CATEGORY ##################################


class ProductListByCategoryView(ListView):
    model = Product
    template_name = (
        "categories.html"  # Use the same template to display products in a category
    )
    context_object_name = "products"
    paginate_by = 10  # Optional: add pagination

    def get_queryset(self):
        # Retrieve the category ID from the URL parameters
        category_id = self.kwargs.get("category_id")
        filter_available_products = self.request.GET.get(
            "filter_available_products", False
        )

        # Filter products by category and optionally by availability
        queryset = Product.objects.filter(category_id=category_id)

        if filter_available_products:
            queryset = queryset.filter(is_available=True)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add the selected category to the context
        category_id = self.kwargs.get("category_id")
        context["category"] = Category.objects.get(id=category_id)

        # Always include the category list in the sidebar
        filter_available_products = self.request.GET.get(
            "filter_available_products", False
        )
        if filter_available_products:
            categories = (
                Category.objects.annotate(
                    available_products_count=Count(
                        "product", filter=Q(product__is_available=True)
                    )
                )
                .filter(available_products_count__gt=0)
                .order_by("-available_products_count")
            )
        else:
            categories = Category.objects.all()

        context["categories"] = categories

        return context


######################## CONTACT VIEW ##################################
######################## CONTACT VIEW ##################################
######################## CONTACT VIEW ##################################
######################## CONTACT VIEW ##################################
######################## CONTACT VIEW ##################################


class ContactPage(TemplateView):
    template_name = "contact.html"


######################## ABOUT VIEW ##################################
######################## ABOUT VIEW ##################################
######################## ABOUT VIEW ##################################
######################## ABOUT VIEW ##################################
######################## ABOUT VIEW ##################################


class AboutPage(TemplateView):
    template_name = "about.html"


######################## PRODUCT DETAIL VIEW ##################################
######################## PRODUCT DETAIL VIEW ##################################
######################## PRODUCT DETAIL VIEW ##################################
######################## PRODUCT DETAIL VIEW ##################################
######################## PRODUCT DETAIL VIEW ##################################


class ProductDetailView(TemplateView):
    template_name = "product_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = kwargs["slug"]
        product = Product.objects.get(slug=slug)
        product.view_count += 1
        product.save()
        context["product"] = product
        return context


######################## ADD TO CART VIEW ##################################
######################## ADD TO CART VIEW ##################################
######################## ADD TO CART VIEW ##################################
######################## ADD TO CART VIEW ##################################
######################## ADD TO CART VIEW ##################################
class AddToCartView(View):
    def get(self, request, product_id):
        # Get or create the cart ID in the session
        cart_id = request.session.get("cart_id", None)

        if cart_id:
            try:
                cart_obj = Cart.objects.get(id=cart_id)
            except Cart.DoesNotExist:
                # Create a new cart if the old one is missing
                cart_obj = Cart.objects.create(total=0)
                request.session["cart_id"] = cart_obj.id
        else:
            # No cart ID in session, create a new cart
            cart_obj = Cart.objects.create(total=0)
            request.session["cart_id"] = cart_obj.id

        # Get the product
        product_obj = get_object_or_404(Product, id=product_id)

        # Check if the product is already in the cart
        cart_product, created = CartProduct.objects.get_or_create(
            cart=cart_obj,
            product=product_obj,
            defaults={"rate": product_obj.selling_price, "quantity": 0, "subtotal": 0},
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
        return redirect("cart_view")


######################## CART VIEW ##################################
######################## CART VIEW ##################################
######################## CART VIEW ##################################
######################## CART VIEW ##################################
######################## CART VIEW ##################################

class CartView(TemplateView):
    template_name = "cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)

        # Retrieve the cart if it exists
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = None

        context["cart"] = cart
        return context


######################## MANAGE CART ##################################
######################## MANAGE CART ##################################
######################## MANAGE CART ##################################
######################## MANAGE CART ##################################
######################## MANAGE CART ##################################

class ManageCart(View):
    def get(self, request, *args, **kwargs):
        cp_id = self.kwargs["cp_id"]
        action = request.GET.get("action")
        cartproduct_obj = get_object_or_404(CartProduct, id=cp_id)
        cart_obj = cartproduct_obj.cart

        if action == "inc":
            cartproduct_obj.quantity += 1
            cartproduct_obj.subtotal = cartproduct_obj.quantity * cartproduct_obj.rate
            cartproduct_obj.save()
            cart_obj.total = sum(
                item.subtotal for item in cart_obj.cartproduct_set.all()
            )
            cart_obj.save()
        elif action == "dec":
            if cartproduct_obj.quantity > 1:
                cartproduct_obj.quantity -= 1
                cartproduct_obj.subtotal = (
                    cartproduct_obj.quantity * cartproduct_obj.rate
                )
                cartproduct_obj.save()
                cart_obj.total = sum(
                    item.subtotal for item in cart_obj.cartproduct_set.all()
                )
                cart_obj.save()
            else:
                cartproduct_obj.delete()
                cart_obj.total = sum(
                    item.subtotal for item in cart_obj.cartproduct_set.all()
                )
                cart_obj.save()
        elif action == "rmv":
            cart_obj.total -= cartproduct_obj.subtotal
            cartproduct_obj.delete()
            cart_obj.save()

        return redirect("cart_view")


######################## EMPTY CART ##################################
######################## EMPTY CART ##################################
######################## EMPTY CART ##################################
######################## EMPTY CART ##################################
######################## EMPTY CART ##################################

class EmptyCart(View):
    def get(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id", None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            if cart.cartproduct_set.exists():
                cart.cartproduct_set.all().delete()
                cart.total = 0
                cart.save()
                messages.success(request, "Cart has been emptied successfully.")
            else:
                messages.info(request, "There are no products in the cart.")
        else:
            messages.info(request, "There is no cart to empty.")
        return redirect("cart_view")
    

######################## CHECKOUT ##################################
######################## CHECKOUT ##################################
######################## CHECKOUT ##################################
######################## CHECKOUT ##################################
######################## CHECKOUT ##################################

class Checkout(CreateView):
    template_name = 'checkout.html'
    form_class = CheckoutForm
    success_url = reverse_lazy('home')
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get('cart_id', None)
        if cart_id:
            try:
                cart_obj = Cart.objects.get(id=cart_id)
                if not cart_obj.cartproduct_set.exists():
                    messages.info(self.request, "Your cart is empty.")
                    cart_obj = None
            except Cart.DoesNotExist:
                cart_obj = None
        else:
            cart_obj = None
        context['cart'] = cart_obj
        return context
    

######################## PLACE ORDER ##################################
######################## PLACE ORDER ##################################
######################## PLACE ORDER ##################################
######################## PLACE ORDER ##################################
######################## PLACE ORDER ##################################

    def form_valid(self, form):
        cart_id = self.request.session.get('cart_id')
        print(f"Cart ID from session: {cart_id}")
        print(Cart.objects.filter(id=3).exists())
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            form.instance.cart = cart_obj
            form.instance.subtotal = cart_obj.total
            form.instance.discount = 0  # Add logic here if you have a discount system
            form.instance.total = cart_obj.total  # Adjust as needed for discounts
            form.instance.order_status = 'Order Received'
            del self.request.session['cart_id']
        else:
            return redirect('home')  # Redirect if no cart ID is found in session

        return super().form_valid(form)
    
class CustomerRegister(CreateView):
    template_name ='register.html'
    form_class = CustomerRegisterForm
    success_url = reverse_lazy('app:home')

    


