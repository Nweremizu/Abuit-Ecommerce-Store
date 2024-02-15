from django.utils import timezone

from django.http import JsonResponse
from django.template.loader import render_to_string

from core.models import Book, Category
from django.db.models import Min, Max


# to get the auy=
def default(request):

    year = timezone.now().year

    min_max = Book.objects.aggregate(Min("price"), Max("price"))
    cart_data = request.session["cart_data_obj"] if "cart_data_obj" in request.session else {}
    if len(cart_data) == 0:
        cart_is_empty = {"cart_is_empty": 1}
        request.session["cart_is_empty"] = cart_is_empty
    else:
        cart_is_empty = {"cart_is_empty": 0}
        request.session["cart_is_empty"] = cart_is_empty


    return {
        'year': year,
        "min_max_price": min_max,
        "cart_is_empty": cart_is_empty,
        "cart_data": cart_data,
        "total_cart_items": len(cart_data),
        "total_cart_price": sum(
            [float(cart_data[book]['price']) * float(cart_data[book]['quantity']) for book in cart_data]),
    }


def side_cart(request):
    cart_data = request.session['cart_data_obj']
    context = {
        "cart_data": cart_data,
        "total_cart_items": len(cart_data),
        "total_cart_price": sum(
            [float(cart_data[book]['price']) * float(cart_data[book]['quantity']) for book in cart_data]),
    }
    data = render_to_string("core/async/cart.html", context)
    return JsonResponse({
        "data": data,
})