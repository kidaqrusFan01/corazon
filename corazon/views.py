from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.db.models import Q
from .models import Product, Order, OrderItem, Category
from django.contrib.auth.decorators import login_required


def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'home.html', {
        'products': products,
        'categories' : categories
        })

def category_products(request, slug):

    category = get_object_or_404(
        Category,
        slug=slug
    )

    products = Product.objects.filter(
        category=category
    )

    categories = Category.objects.all()

    return render(
        request,
        "category.html",
        {
            "category": category,
            "products": products,
            "categories": categories
        }
    )

def search_products(request):

    query = request.GET.get("q")

    products = Product.objects.filter(

        Q(title__icontains=query) |

        Q(description__icontains=query)

    )

    categories = Category.objects.all()

    return render(
        request,
        "search_results.html",
        {
            "query": query,
            "products": products,
            "categories": categories
        }
    )

@login_required
def submit_review(request, pk):

    product = get_object_or_404(
        Product,
        pk=pk
    )

    rating = request.POST.get(
        'rating'
    )

    comment = request.POST.get(
        'comment'
    )

    Review.objects.update_or_create(

        user=request.user,

        product=product,

        defaults={
            'rating': rating,
            'comment': comment
        }
    )

    return redirect(
        'product_detail',
        pk=pk
    )

@login_required
def dashboard(request):

    products = Product.objects.filter(
        seller=request.user
    )

    return render(
        request,
        'dashboard.html',
        {
            'products': products
        }
    )

def product_detail(request, pk):

    product = get_object_or_404(
        Product,
        pk=pk
    )

    related_products = Product.objects.filter(
        category=product.category
    ).exclude(
        id=product.id
    )[:4]

    return render(
        request,
        'product_detail.html',
        {
            'product': product,
            'related_products': related_products
        }
    )

def add_product(request):

    if request.method == "POST":

        title = request.POST.get("title")
        description = request.POST.get("description")
        price = request.POST.get("price")
        stock = request.POST.get("stock")
        image = request.FILES.get("image")

        Product.objects.create(
            seller=request.user,
            title=title,
            description=description,
            price=price,
            stock=stock,
            image=image
        )

        return redirect("dashboard")

    return render(
        request,
        "add_product.html"
    )

@login_required
def add_to_wishlist(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    return redirect(
        'product_detail',
        pk=product.id
    )

def ajax_add_to_cart(request, product_id):

    cart = request.session.get("cart", {})

    cart[str(product_id)] = (
        cart.get(str(product_id), 0) + 1
    )

    request.session["cart"] = cart

    return JsonResponse({
        "success": True,
        "cart_count": sum(cart.values())
    })


def add_to_cart(request, product_id):

    cart = request.session.get("cart", {})

    cart[str(product_id)] = (
        cart.get(str(product_id), 0) + 1
    )

    request.session["cart"] = cart

    return redirect("cart")


def cart_view(request):

    cart = request.session.get("cart", {})

    cart_items = []
    total = 0

    for product_id, quantity in cart.items():

        product = Product.objects.get(id=product_id)

        subtotal = product.price * quantity

        total += subtotal

        cart_items.append({
            "product": product,
            "quantity": quantity,
            "subtotal": subtotal
        })

    return render(
        request,
        "cart.html",
        {
            "cart_items": cart_items,
            "total": total
        }
    )

def increase_quantity(request, product_id):

    cart = request.session.get("cart", {})

    cart[str(product_id)] += 1

    request.session["cart"] = cart

    return redirect("cart")

def decrease_quantity(request, product_id):

    cart = request.session.get("cart", {})

    if cart[str(product_id)] > 1:
        cart[str(product_id)] -= 1
    else:
        del cart[str(product_id)]

    request.session["cart"] = cart

    return redirect("cart")

def remove_item(request, product_id):

    cart = request.session.get("cart", {})

    if str(product_id) in cart:
        del cart[str(product_id)]

    request.session["cart"] = cart

    return redirect("cart")

def checkout(request):
    cart = request.session.get('cart', {})

    if not cart:
        return redirect('home')

    order = Order.objects.create(user=request.user)

    total = 0

    for product_id, qty in cart.items():
        product = Product.objects.get(id=product_id)

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=qty,
            price=product.price
        )

        total += product.price * qty

    order.total_price = total
    order.save()

    request.session['cart'] = {}

    return render(request, 'checkout_success.html', {'order': order})