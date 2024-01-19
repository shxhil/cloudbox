from django.urls import path

from store import views

from rest_framework.authtoken.views import ObtainAuthToken

from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register("products",views.productsView,basename="products")


urlpatterns = [
    path("register/",views.SignupView.as_view()),
    path("token/",ObtainAuthToken.as_view()),

]+router.urls
