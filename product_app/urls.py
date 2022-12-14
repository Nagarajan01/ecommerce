from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'product_app'

urlpatterns = [
    path('listjson/', views.listjson.as_view(), name="listjson"),
    path('register/', views.registerPage, name="register"),
    path('view_cart/', views.view_cart.as_view(), name="view_cart"),
    path('view_cart_json/', views.view_cart_json.as_view(), name="view_cart_json"),
    path('accounts/login/', views.loginPage, name="login"),
    path('lists/', login_required(views.Lists.as_view()), name="Lists"),
    path('logout/', views.logoutUser, name="logout"),
    path('cart/<int:id>', views.add_to_cart, name="add_to_cart"),
    path('order_results/', views.order_results, name="order_results"),
    path('updatecart/', views.cart_update, name="updatecart"),
    path('order_view/', views.order_view, name="order_view"),
    path('wishlist/<int:id>', views.add_to_wishlist, name="wishlist"),
    path('removewishlist/<int:id>', views.removewishlist, name="removewishlist"),
    path('updateorder/', views.updateorder, name="removeorder"),
    path('view_wishlist/', login_required(views.view_wishlist.as_view()), name="viewwishlist"),
    path('home',
         views.get_queryset, name="SearchResultsView"), 
    path('checkout/',
         views.checkout, name="checkout"), 
    path('success/', views.SuccessView.as_view(), name='success'),
    path('cancel/', views.CancelView.as_view(), name='cancel'),
    path('webhook', views.stripe_webhook, name='stripe_webhook'),

]
