from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from core.forms import ShippingAddressForm
from core.models import Book, CartOrder, CartOrderItem, Address, Category
from django.template.loader import render_to_string
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from core.conversion import paypalCurrencyConverter
from core.forms import ExtraPayPalForm


def custom_404(request, exception):
    return render(request, 'error/404.html', status=404)


# Create your views here.
def index(request):
    books = Book.objects.all().order_by("-date_added")[:4]

    context = {
        "books": books
    }
    return render(request, "core/index.html", context)


def profile(request):
    if not request.user.is_authenticated:
        return redirect('abuit_user:login')
    user = request.user
    return render(request, "core/profile.html", {"user": user})


def books_list(request):
    Books = Book.objects.all().order_by("-date_added")
    authors = Book.objects.values_list('author', flat=True).distinct()
    categories = Category.objects.all()

    context = {
        "Books": Books,
        "authors": authors,
        "categories": categories,
    }
    return render(request, 'core/product list.html', context)


def book_detail(request, bid):
    book = get_object_or_404(Book, bid=bid)
    related_books = Book.objects.filter(category=book.category).exclude(bid=bid)[:4]
    context = {
        "book": book,
        "related_books": related_books,
    }
    return render(request, 'core/product_detail.html', context=context)


def search_view(request):
    query = request.GET.get("search-query")
    Books = Book.objects.filter(title__icontains=query).order_by('-date_added')
    context = {
        "Books": Books,
        'query': query
    }
    return render(request, 'core/search_page.html', context=context)


def filter_books(request):
    categories = request.GET.getlist('category[]')
    authors = request.GET.getlist('author[]')

    min_price = int(request.GET.get('min_price'))
    max_price = request.GET.get('max_price')
    radio = request.GET.get('radio')
    radio = True if radio == "1" else False
    if radio is None:
        radio = True

    products = Book.objects.all().order_by('-date_added').distinct()

    products = products.filter(in_stock=radio).order_by('-date_added').distinct()

    if min_price and max_price:
        products = products.filter(price__gte=min_price, price__lte=max_price)

    if len(categories) > 0:
        products = products.filter(category__cid__in=categories).distinct()

    if len(authors) > 0:
        products = products.filter(author__in=authors).distinct()

    context = {"products": products}
    data = render_to_string("core/async/product-list.html", context)
    return JsonResponse({
        "data": data,
    })


def add_to_cart(request):
    # If user is not logged in redirect to login page and do not proceed further

    cart_book = {str(request.GET.get('book_id')): {
        'title': request.GET.get('book_title'),
        'price': request.GET.get('book_price'),
        'image': request.GET.get('book_image'),
        'quantity': request.GET.get('quantity'),
        'category': request.GET.get('book_category'),
        'author': request.GET.get('book_author'),
    }}

    if 'cart_data_obj' in request.session:
        if str(request.GET.get('book_id')) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET.get('book_id'))]['quantity'] = int(
                cart_book[str(request.GET.get('book_id'))]['quantity']) + int(
                cart_data[str(request.GET.get('book_id'))]['quantity'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_book)
            request.session['cart_data_obj'] = cart_data
    else:
        request.session['cart_data_obj'] = cart_book

    return JsonResponse({"data": request.session['cart_data_obj'],
                         'total_cart_items': len(request.session['cart_data_obj'])
                         })


def cart_view(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Please Login to view your cart.")
        return redirect('abuit_user:login')

    if 'cart_data_obj' in request.session:
        cart_data = request.session['cart_data_obj']
        total_cart_items = len(request.session['cart_data_obj'])
        total_cart_price = sum(
            [float(cart_data[book]['price']) * float(cart_data[book]['quantity']) for book in cart_data])
    else:
        cart_data = {}
        total_cart_items = 0
        total_cart_price = 0

    context = {
        "cart_data": cart_data,
        "total_cart_items": total_cart_items,
        "total_cart_price": total_cart_price,
    }
    return render(request, 'core/cart.html', context=context)


def update_cart(request):
    cart_data = request.session['cart_data_obj']
    cart_data[str(request.GET.get('book_id'))]['quantity'] = int(request.GET.get('quantity'))
    request.session['cart_data_obj'] = cart_data
    context = {
        "cart_data": request.session['cart_data_obj'],
        "total_cart_items": len(cart_data),
        "total_cart_price": sum(
            [float(cart_data[book]['price']) * float(cart_data[book]['quantity']) for book in cart_data]),
    }
    data = render_to_string("core/async/cart.html", context)
    return JsonResponse({
        "data": data,
    })


def delete_cart_item(request):
    cart_data = request.session['cart_data_obj']
    del cart_data[str(request.GET.get('book_id'))]
    request.session['cart_data_obj'] = cart_data
    context = {
        "cart_data": request.session['cart_data_obj'],
        "total_cart_items": len(cart_data),
        "total_cart_price": sum(
            [float(cart_data[book]['price']) * float(cart_data[book]['quantity']) for book in cart_data]),
    }
    data = render_to_string("core/async/cart.html", context)
    return JsonResponse({
        "data": data,
    })


def check_cart(request):
    cart_is_empty = {}
    if request.session['cart_data_obj']:
        if len(request.session['cart_data_obj']) == 0:
            cart_is_empty = {"cart_is_empty": 1}
            request.session["cart_is_empty"] = cart_is_empty
        else:
            cart_is_empty = {"cart_is_empty": 0}
            request.session["cart_is_empty"] = cart_is_empty
        return JsonResponse({
            "data": cart_is_empty,
        })
    else:
        request.session['cart_data_obj'] = {}


def side_cart(request):
    cart_data = request.session['cart_data_obj']
    if str(request.GET.get('book_id')) in cart_data:
        quantity = cart_data[str(request.GET.get('book_id'))]['quantity']
    context = {
        "cart_data": cart_data,
        "total_cart_items": len(cart_data),
        "total_cart_price": sum(
            [float(cart_data[book]['price']) * float(cart_data[book]['quantity']) for book in cart_data]),
    }
    if str(request.GET.get('book_id')) in cart_data:
        quantity = cart_data[str(request.GET.get('book_id'))]['quantity']
        context.update({"quantity": quantity})
    data = render_to_string("core/async/m_cart.html", context)
    return JsonResponse({
        "data": data,
    })


@login_required
def checkout_view(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Please Login to view your cart.")
        return redirect('abuit_user:login')

    if 'cart_data_obj' in request.session:
        cart_data = request.session['cart_data_obj']
        total_cart_items = len(request.session['cart_data_obj'])
        total_amount_of_each = {book: float(cart_data[book]['price']) * float(cart_data[book]['quantity']) for book in
                                cart_data}
        shipping_cost = sum([200 * float(cart_data[book]['quantity']) for book in cart_data])
        total_cart_price = sum(
            [float(cart_data[book]['price']) * float(cart_data[book]['quantity']) for book in cart_data])
        full_total = total_cart_price + shipping_cost

        order = CartOrder.objects.create(user=request.user, total_amount=full_total)

        for book_id, item in request.session['cart_data_obj'].items():
            cart_total = float(item['price']) * float(item['quantity'])
            book = Book.objects.get(bid=book_id)
            CartOrderItem.objects.create(order=order, invoice_number=f"Invoice-No-{order.id}", book=book,
                                         quantity=item['quantity'], image=item['image'], price=item['price'],
                                         total=total_amount_of_each[book_id])

    else:
        cart_data = {}
        total_cart_items = 0
        total_cart_price = 0
        shipping_cost = 0
        full_total = 0

    host = request.get_host()
    amount = paypalCurrencyConverter(full_total)
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': amount,
        'item_name': f'Order-item-NO-{order.id}',
        'invoice': f"Invoice-No-{order.id}",
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host, reverse('core:paypal-ipn')),
        'return_url': 'http://{}{}'.format(host, reverse('core:payment-success')),
        'cancel_return': 'http://{}{}'.format(host, reverse('core:payment-failed')),
    }
    paypal_payment_button = ExtraPayPalForm(initial=paypal_dict)

    user = request.user
    first_name = user.first_name
    last_name = user.last_name

    context = {
        "cart_data": cart_data,
        "total_cart_items": total_cart_items,
        "total_cart_price": total_cart_price,
        "shipping_cost": shipping_cost,
        "full_total": full_total,
        "paypal_payment_button": paypal_payment_button,
    }
    return render(request, 'core/checkout.html', context)


@login_required
def payment_success(request):
    if 'cart_data_obj' in request.session:
        cart_data = request.session['cart_data_obj']
        total_cart_items = len(request.session['cart_data_obj'])
        for book in cart_data:
            cart_data[book]['total_amount'] = float(cart_data[book]['price']) * float(cart_data[book]['quantity'])
        shipping_cost = sum([200 * float(cart_data[book]['quantity']) for book in cart_data])
        total_cart_price = sum(
            [float(cart_data[book]['price']) * float(cart_data[book]['quantity']) for book in cart_data])
        full_total = total_cart_price + shipping_cost
    else:
        cart_data = {}
        total_cart_items = 0
        total_cart_price = 0
        shipping_cost = 0
        full_total = 0

    context = {
        "cart_data": cart_data,
        "total_cart_items": total_cart_items,
        "total_cart_price": total_cart_price,
        "shipping_cost": shipping_cost,
        "full_total": full_total,
    }
    return render(request, 'core/payment_complete.html', context)


@login_required
def payment_declined(request):
    return render(request, 'core/payment_declined.html')
