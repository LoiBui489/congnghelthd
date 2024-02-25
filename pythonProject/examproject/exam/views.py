from django.db import transaction
from rest_framework import viewsets, generics, parsers, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from . import serializers, perms, dao
from .models import Category, Product, User, Follow, Comment, Rating, Order, MyOrderProduct, Department, Menu, \
    MyMenuProduct, MyMenuDepartment
from .properties import STATUS_DOING
from .serializers import CategorySerializer, ProductSerializer, UserSerializer, FollowSerializer, CommentSerializer, \
    RatingSerializer, OrderSerializer, OrderDetailSerializer, MenuSerializer, MenuDetailSerializer, \
    MyMenuDepartmentSerializer


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView, generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = [parsers.MultiPartParser]

    def get_permissions(self):
        if self.action.__eq__('get_current_user'):
            return [permissions.IsAuthenticated()]
        if self.action.__eq__('patch_is_active'):
            return [permissions.IsAuthenticated(), perms.IsAdminPermission()]

        return [permissions.AllowAny()]

    @action(methods=['get'], url_path='current-user', url_name='current-user', detail=False)
    def get_current_user(self, request):
        return Response(serializers.UserSerializer(request.user).data)

    @action(methods=['patch'], url_path='active-user/(?P<pk>[^/.]+)', url_name='active-user', detail=False)
    def patch_is_active(self, request, pk):
        user = self.get_object()
        if user:
            user.is_active = True
            user.save()
            return Response(serializers.UserSerializer(user).data, status=status.HTTP_200_OK)
        return Response(Serializer(data={'detail': 'Item not found!'}).initial_data, status=status.HTTP_404_NOT_FOUND)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(active=True)
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView):
    queryset = Product.objects.filter(active=True)
    serializer_class = ProductSerializer

    def get_queryset(self):
        queries = self.queryset

        kw = self.request.query_params.get('kw')
        if kw:
            queries = queries.filter(name__icontains=kw)

        cate_id = self.request.query_params.get('cateId')
        if cate_id:
            queries = queries.filter(category_id=cate_id)

        dpt_id = self.request.query_params.get('dptId')
        if dpt_id:
            queries = queries.filter(department_id=cate_id)

        fpr = self.request.query_params.get('fpr')
        if fpr:
            queries = queries.filter(price__gte=int(fpr))

        tpr = self.request.query_params.get('tpr')
        if tpr:
            queries = queries.filter(price__lte=int(tpr))

        return queries


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.filter(active=True)
    serializer_class = FollowSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.filter(active=True)
    serializer_class = CommentSerializer


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.filter(active=True)
    serializer_class = RatingSerializer


class OrderViewSet(viewsets.ViewSet, generics.ListAPIView, generics.UpdateAPIView):
    queryset = Order.objects.filter(active=True)
    serializer_class = OrderSerializer

    @action(methods=['post'], detail=False, url_name='order', url_path='create-order')
    @transaction.atomic
    def create_order(self, request):
        o = request.data.get('order')
        d = Department.objects.filter(id=o['department']).first()
        u = User.objects.filter(id=o['ordered_user']).first()
        od = []
        total = 0

        o.update({"status": STATUS_DOING})
        o.update({"shipping_fee": d.shipping_fee})
        o.update({"department": d})
        o.update({"ordered_user": u})
        o.update({"total_fee": total + o['shipping_fee']})

        with transaction.atomic():
            order = Order(**o)
            order.save()
            for c in request.data.get('cart'):
                with transaction.atomic():
                    p = Product.objects.filter(id=c['product']).first()
                    order_detail = MyOrderProduct.objects.create(order=order, product=p,
                                                                 product_price=c['product_price'],
                                                                 quantity=c['quantity'],
                                                                 user_request=c['user_request'])
                    total += order_detail.product_price * order_detail.quantity
                    od.append(OrderDetailSerializer(order_detail).data)

            order.total_fee += total
            order.save()

            result = OrderSerializer(order).data
            result.update({'order_detail': od})
            return Response(result, status=status.HTTP_201_CREATED)


class OrderDetailViewSet(viewsets.ViewSet, generics.ListCreateAPIView):
    queryset = MyOrderProduct.objects.filter(active=True)
    serializer_class = OrderDetailSerializer


class MenuViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Menu.objects.filter(active=True)
    serializer_class = MenuSerializer


class MenuDetailViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = MyMenuProduct.objects.filter(active=True)
    serializer_class = MenuDetailSerializer


class MyMenuDepartmentViewSet(viewsets.ViewSet, generics.ListCreateAPIView, generics.UpdateAPIView):
    queryset = MyMenuDepartment.objects.filter(active=True)
    serializer_class = MyMenuDepartmentSerializer


class StatisticViewSet(viewsets.ViewSet):
    @action(methods=['get'], detail=False, url_path='revenue-product', url_name='revenue')
    def revenue_statistic_by_product(self, request):
        params = {
            "year": 2023,
            "month": 2
        }
        revenue = dao.revenue_statistic_by_product(params)
        return Response(Serializer(data=revenue).initial_data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='revenue-category', url_name='revenue')
    def revenue_statistic_by_category(self, request):
        params = {
            "year": 2023,
            "month": 2
        }
        revenue = dao.revenue_statistic_by_category(params)
        return Response(Serializer(data=revenue).initial_data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='department-selling', url_name='revenue')
    def department_selling_product_statistic(self, request):
        result = dao.department_selling_product_statistic('quarter')
        return Response(Serializer(data=result).initial_data, status=status.HTTP_200_OK)
