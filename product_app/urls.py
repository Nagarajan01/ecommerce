from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'product_app'

urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('view_cart/', views.view_cart.as_view(), name="view_cart"),
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
]


#path('search/', views.index.as_view(), name="search"),
#
# view_cart/orders/{{i.id}}
#path('search_results/', views.SearchResultsView.as_view(), name="SearchResultsView"),
