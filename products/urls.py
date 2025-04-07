from django.urls import path
from . import views

urlpatterns = [
    path('product', views.product, name='product'),
    # path('<int:product_id>', views.delete_product, name='delete_product')
]   