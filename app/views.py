

from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import TemplateView, ListView, View, CreateView, FormView, DetailView
from app.models import *
from django.core.paginator import Paginator
from django.db.models import Count, Q
from .models import Category
from django.contrib import messages
from app.forms import CheckoutForm, CustomerRegisterForm, CustomerLoginForm, AdminLoginForm
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login,logout



class AppMixin(object):
    def dispatch(self, request, *args, **kwargs):
        cart_id = request.session.get('cart_id')
        if cart_id:
            cart_obj = Cart.objects.get(id = cart_id)
            if request.user.is_authenticated and request.user.customer:
                cart_obj.customer = request.user.customer
                cart_obj.save()
        return super().dispatch(request, *args, **kwargs)
    
######################## HOME VIEW ##################################
######################## HOME VIEW ##################################
######################## HOME VIEW ##################################
######################## HOME VIEW ##################################
######################## HOME VIEW ##################################


class HomePage(AppMixin,TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.all().order_by("-id")
        paginator = Paginator(products,8)
        page_number = self.request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        context["page_obj"] = page_obj

        return context


######################## CATEGORY VIEW ##################################
######################## CATEGORY VIEW ##################################
######################## CATEGORY VIEW ##################################
######################## CATEGORY VIEW ##################################
######################## CATEGORY VIEW ##################################


class CategoryView(AppMixin,TemplateView):
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
        paginator = Paginator(products,6)
        page_number = self.request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        context["page_obj"] = page_obj
        # Add categories and products to context
        context["categories"] = categories
        context["page_obj"] = page_obj

        return context


######################## PRODUCT LIST BY CATEGORY ##################################
######################## PRODUCT LIST BY CATEGORY ##################################
######################## PRODUCT LIST BY CATEGORY ##################################
######################## PRODUCT LIST BY CATEGORY ##################################
######################## PRODUCT LIST BY CATEGORY ##################################


class ProductListByCategoryView(AppMixin,ListView):
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


class ContactPage(AppMixin,TemplateView):
    template_name = "contact.html"


######################## ABOUT VIEW ##################################
######################## ABOUT VIEW ##################################
######################## ABOUT VIEW ##################################
######################## ABOUT VIEW ##################################
######################## ABOUT VIEW ##################################


class AboutPage(AppMixin,TemplateView):
    template_name = "about.html"


######################## PRODUCT DETAIL VIEW ##################################
######################## PRODUCT DETAIL VIEW ##################################
######################## PRODUCT DETAIL VIEW ##################################
######################## PRODUCT DETAIL VIEW ##################################
######################## PRODUCT DETAIL VIEW ##################################


class ProductDetailView(AppMixin,TemplateView):
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
class AddToCartView(AppMixin,View):
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
        return redirect("app:cart_view")


######################## CART VIEW ##################################
######################## CART VIEW ##################################
######################## CART VIEW ##################################
######################## CART VIEW ##################################
######################## CART VIEW ##################################

class CartView(AppMixin,TemplateView):
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

class ManageCart(AppMixin,View):
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

        return redirect("app:cart_view")


######################## EMPTY CART ##################################
######################## EMPTY CART ##################################
######################## EMPTY CART ##################################
######################## EMPTY CART ##################################
######################## EMPTY CART ##################################

class EmptyCart(AppMixin,View):
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
        return redirect("app:cart_view")
    

######################## CHECKOUT ##################################
######################## CHECKOUT ##################################
######################## CHECKOUT ##################################
######################## CHECKOUT ##################################
######################## CHECKOUT ##################################

class Checkout(AppMixin,CreateView):
    template_name = 'checkout.html'
    form_class = CheckoutForm
    success_url = reverse_lazy('app:home')
    

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.customer:
            pass
        else:
            return redirect('/login/?next=/Checkout/')
        return super().dispatch(request, *args, **kwargs)
        
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
            return redirect('app:home')  # Redirect if no cart ID is found in session

        return super().form_valid(form)
    

######################## Customer Registration ##################################
######################## Customer Registration ##################################
######################## Customer Registration ##################################
######################## Customer Registration ##################################
######################## Customer Registration ##################################

class CustomerRegister(CreateView):
    template_name = 'register.html'
    form_class = CustomerRegisterForm
    success_url = reverse_lazy('app:home')

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        full_name = form.cleaned_data.get("full_name")
        address = form.cleaned_data.get("address")
            # Create the user and customer
        user = User.objects.create_user(username, email, password)
        Customer.objects.create(user=user, full_name=full_name, address=address)
        login(self.request, user)
            
            # Add a success message and redirect

        return redirect(self.success_url)
    
    def get_success_url(self):
    # If a 'next' parameter is provided in the URL, redirect there
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url
        

######################## Customer Logout ##################################
######################## Customer Logout ##################################
######################## Customer Logout ##################################
######################## Customer Logout ##################################
######################## Customer Logout ##################################         

class CustomerLogout(View):
    def get(self,request):
        logout(request)
        return redirect('app:home')


######################## Customer Login ##################################
######################## Customer Login ##################################
######################## Customer Login ##################################
######################## Customer Login ##################################
######################## Customer Login ##################################

class CustomerLogin(FormView):
    template_name = 'login.html'
    form_class = CustomerLoginForm
    success_url = reverse_lazy('app:home')

    # FORM VALID METHOD IS A TYPE OF METHOD AND IS AVILIABLE IN CREATEVIEW , FORMVIEW, AND UPDATEVIEW
    def form_valid(self, form):
        uname = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username = uname, password = password)
        if user is not None and Customer.objects.filter(user=user).exists():
            login(self.request, user)
        else:
            return render(self.request, 'login.html', {'form': self.form_class, "error": "Please Check the Username and Password"})
        return super().form_valid(form)
    
    def get_success_url(self):
    # If a 'next' parameter is provided in the URL, redirect there
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url
        
class CustomerProfile(TemplateView):
    template_name = 'profile.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect('/login/?next=/profile/')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        customer = self.request.user.customer
        orders = Order.objects.filter(cart__customer=customer).order_by('-id')
        context['orders'] = orders
        context['customer'] = customer
        return context
class CustomerOrderDetail(DetailView):
    template_name = 'orderdetail.html'
    model = Order
    context_object_name = 'order_obj'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            order_id = self.kwargs['pk']
            order = Order.objects.get(id = order_id)
            if request.user.customer != order.cart.customer:
                return redirect('app:customerprofile')
        else:
            return redirect('/login/?next=/profile/')
        return super().dispatch(request, *args, **kwargs)
    
class Search(TemplateView):
    template_name = 'search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        keyword = self.request.GET.get('keyword')

        if keyword:
            # Search in both `title` and `category__name`
            result = Product.objects.filter(
                Q(title__icontains=keyword) | Q(category__title__icontains=keyword) | Q(description__icontains=keyword) | Q(return_policy__icontains=keyword)
            ).distinct()
        else:
            result = Product.objects.none()  # No results if no keyword

        context['result'] = result
        return context
###################################################################### Admin Login ###############################################################

class AdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Admin.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect('/admin_login/')
        return super().dispatch(request, *args, **kwargs)

class AdminLogin(AdminRequiredMixin,FormView):
    template_name = 'AdminPanel/adminlogin.html'
    form_class = AdminLoginForm
    success_url = reverse_lazy('app:adminhome')

    def form_valid(self, form):
        uname = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username = uname, password = password)
        if user is not None and Admin.objects.filter(user=user).exists():
            login(self.request, user)
        else:
            return render(self.request, self.template_name, {'form': self.form_class, "error": "Please Check the Username and Password"})
        return super().form_valid(form)


class AdminHomePage(AdminRequiredMixin,TemplateView):
    template_name = 'AdminPanel/adminhome.html'

    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pendingorders'] = Order.objects.filter(
            order_status ='Order Received'
        ).order_by('-id')
        return context
    
class AdminOrderDetail(AdminRequiredMixin,DetailView):
    template_name = 'AdminPanel/orderdetail.html'
    model = Order
    context_object_name = 'order_obj'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status'] = ORDER_STATUS
        return context

class AdminAllOrder(AdminRequiredMixin,ListView):
    template_name = 'AdminPanel/allorderlist.html'
    queryset = Order.objects.all().order_by('-id')
    context_object_name = 'order_obj'
    
class AdminOrderStatusChange(AdminRequiredMixin,View):
    def post(self, request,*args, **kwargs):
        order_id = self.kwargs['pk']
        order_obj = Order.objects.get(id = order_id)
        new_status = request.POST.get('status')
        order_obj.order_status = new_status
        order_obj.save()
        return redirect(reverse_lazy('app:adminorderdetail', kwargs={'pk': order_id}))
    


    

    


