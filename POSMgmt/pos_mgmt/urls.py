from django.urls import path
from .views import (
    RegisterUserView,
    UserLoginView,
    ItemPurchaseView,
    ItemPurchaseDetailView,
    ItemSalesView,
    StoreView
)


urlpatterns = [
    path("register/", RegisterUserView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("item-purchase/", ItemPurchaseView.as_view(), name="item-purchase"),
    path(
        "item-purchase/detail/<int:pk>/",
        ItemPurchaseDetailView.as_view(),
        name="ItemPurchase-detail",
    ),
    path("item-sales/", ItemSalesView.as_view(), name="item-sales"),
    path("store/", StoreView.as_view(), name="store_view")
]
