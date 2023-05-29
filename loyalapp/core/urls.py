from django.urls import path
from . import views


urlpatterns = [
    path('history/<id>/', views.history,name='history'),
    path('print id/<int:id>/', views.print_id, name='print id'),
    path('', views.index2   ),
    path('send/<phone_number>', views.send, name='send'),
    path('analytics', views.analytics, name='analytics'),
    path('orders', views.getOrders, name='orders'),
]
