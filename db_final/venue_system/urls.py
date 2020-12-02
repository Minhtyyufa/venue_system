from django.urls import path, include
from rest_framework import routers
from .views import views, customer_view

router = routers.DefaultRouter()
router.register(r"customer", customer_view.CustomerViewSet)
router.register(r"roles", views.RoleViewSet)
router.register(r"admin", views.AdminViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]