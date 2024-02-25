from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('categories', views.CategoryViewSet, basename='categories')
router.register('products', views.ProductViewSet, basename='products')
router.register('user', views.UserViewSet, basename='user')
router.register('order', views.OrderViewSet, basename='order')
router.register('order-detail', views.OrderDetailViewSet, basename='order-detail')
router.register('menu', views.MenuViewSet, basename='menu')
router.register('menu-detail', views.MenuDetailViewSet, basename='menu-detail')
router.register('menu-department', views.MyMenuDepartmentViewSet, basename='menu-department')

router.register('follow', views.FollowViewSet, basename='follow')
router.register('comment', views.CommentViewSet, basename='comment')
router.register('rating', views.RatingViewSet, basename='rating')

router.register('statistic', views.StatisticViewSet, basename='statistic')

urlpatterns = [
    path('', include(router.urls)),
]
