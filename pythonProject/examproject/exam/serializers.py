import cloudinary.uploader
from rest_framework.serializers import ModelSerializer

from .models import Category, Product, User, Follow, Comment, Rating, Order, MyOrderProduct, Menu, MyMenuProduct, \
    MyMenuDepartment
from .properties import CLOUDINARY_URL, ROLE_SHOP


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'email', 'avatar', 'role', 'address']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def to_representation(self, instance):
        ret = super(UserSerializer, self).to_representation(instance)
        avatar = ret['avatar']
        if avatar:
            avatar = CLOUDINARY_URL + avatar
            ret.__setitem__('avatar', avatar)

        return ret

    def create(self, validated_data):
        data = validated_data.copy()
        user = User(**data)

        user.set_password(data['password'])

        image = cloudinary.uploader.upload(validated_data['avatar'], folder='foodshop/user')
        image_url = 'v{version}/{public_id}.{format}'.format(version=image['version'],
                                                             public_id=image['public_id'],
                                                             format=image['format'])
        user.avatar = image_url

        if user.role == ROLE_SHOP:
            user.is_active = False

        user.save()

        return user


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category']


class FollowSerializer(ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class RatingSerializer(ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderDetailSerializer(ModelSerializer):
    class Meta:
        model = MyOrderProduct
        fields = '__all__'


class MenuSerializer(ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'

    # here
    def to_representation(self, instance):
        ret = super(MenuSerializer, self).to_representation(instance)

        products = ret['products']
        departments = ret['departments']
        menu_id = ret['id']

        if products:
            products = map(lambda p: MenuDetailSerializer(
                MyMenuProduct.objects
                .filter(menu=menu_id).filter(product=p)
                .first()).data, products)

            ret.__setitem__('products', products)
        if departments:
            departments = map(lambda d: MyMenuDepartmentSerializer(
                MyMenuDepartment.objects
                .filter(menu=menu_id).filter(department=d)
                .first()).data, departments)

            ret.__setitem__('departments', departments)

        return ret


class MenuDetailSerializer(ModelSerializer):
    class Meta:
        model = MyMenuProduct
        fields = ['id', 'menu', 'product', 'product_sell_from_time', 'product_sell_to_time']


class MyMenuDepartmentSerializer(ModelSerializer):
    class Meta:
        model = MyMenuDepartment
        fields = ['id', 'department', 'menu', 'selling_time', 'description']
