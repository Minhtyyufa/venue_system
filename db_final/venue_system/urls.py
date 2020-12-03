from django.urls import path, include
from rest_framework import routers
from .views import views
from venue_system.views.customer_view import CustomerViewSet
from venue_system.views.venue_view import VenueViewSet

router = routers.DefaultRouter()
router.register(r"custom_user", views.CustomUserViewSet)
router.register(r"venue", VenueViewSet)
router.register(r"customer", CustomerViewSet)
router.register(r"user", views.UserViewSet)
router.register(r"roles", views.RoleViewSet)
router.register(r"admin", views.AdminViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]