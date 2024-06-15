from django.urls import path

from . import views

urlpatterns=[
    path('',views.index,name='index'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('cart/',views.cart,name='cart'),
    path('search/',views.search,name='search'),
    path('productview/<int:myid>',views.productview,name='productview'),
    path('checkout/',views.checkout,name='checkout'),
    path('update_item/',views.updateItem,name='update_item'),
    path('cart/update_item/',views.updateItem,name='update_item'),    #to fix fetching url when up down arrows of cart.html are clicked
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('process_order/',views.processOrder,name='process_order'),
]