from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
#from product_app.views import CreateCheckoutSessionView, CancelView, SuccessView, ProductLandingPageView, stripe_webhook

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


#path('search/', views.index.as_view(), name=   "search"),
#
# view_cart/orders/{{i.id}}
#path('search_results/', views.SearchResultsView.as_view(), name="SearchResultsView"),


'''
    path('thanks/', views.thanks, name='thanks'),
    path('checkout/', views.checkout, name='checkout'),
    path('stripe_webhook/', views.stripe_webhook, name='stripe_webhook')'''

'''

      <script src="https://js.stripe.com/v3/"></script>

      <script>

        const buy_now_button = document.querySelector('#buy_now_btn')

        buy_now_button.addEventListener('click', event => {   
          fetch('/checkout/')
          .then((result) => { return result.json() })
          .then((data) => {
            var stripe = Stripe(data.stripe_public_key);

            stripe.redirectToCheckout({
            // Make the id field from the Checkout Session creation API response
            // available to this file, so you can provide it as parameter here
            // instead of the {{CHECKOUT_SESSION_ID}} placeholder.
              sessionId: data.session_id
            }).then(function (result) {
              // If `redirectToCheckout` fails due to a browser or network
              // error, display the localized error message to your customer
              // using `result.error.message`.
            });
          }) 
        })
      </script>''''''
    path('create-payment-intent/<pk>/', StripeIntentView.as_view(), name='create-payment-intent'),
    path('webhooks/stripe/', stripe_webhook, name='stripe-webhook'),'''