from django.urls import path, include
from core import views

app_name = 'core'
urlpatterns = [

    # ---------------Home and Account------------#
    path('', views.index, name='main'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_account_details, name='edit-account'),

    # --------------Books Url-------------------#
    path('books/', views.books_list, name='books'),
    path('books/<bid>', views.book_detail, name='detail'),
    path('filter/', views.filter_books, name='filter-books'),
    path('search/', views.search_view, name='search-view'),

    # --------------Cart Related----------------#
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.cart_view, name='cart-view'),
    path('update_cart/', views.update_cart, name='update-cart'),
    path('delete_cart_item/', views.delete_cart_item, name='delete-cart-item'),
    path('check_cart/', views.check_cart, name='check_cart'),
    path('side_cart/', views.side_cart, name='side-cart'),

    # --------------Checkout And Payment---------#
    path('check_out/', views.checkout_view, name='check-out'),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('payment-success/', views.payment_success, name='payment-success'),
    path('payment-failed/', views.payment_declined, name='payment-failed'),

]
