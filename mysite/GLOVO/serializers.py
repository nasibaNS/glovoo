from  rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'first_name', 'last_name',
                  'age', 'phone_number', 'role')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }




class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'



class UserProfileSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username']



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_name']



class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['title', 'phone_number', 'website']


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_name', 'product_image', 'description', 'price', 'quantity']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'




class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True, source='product')
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'get_total_price']


class CartSerializer(serializers.ModelSerializer):
    cart_item = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = ['id', 'user', 'total_price', 'cart_item']

        def get_total_price(self, obj):
            return obj.get_total_price()



class ProductComboListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCombo
        fields = ['combo_name', 'combo_image', 'combo_price', 'description']


class ProductComboSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCombo
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField('%d-%m-%Y')
    class Meta:
        model = Order
        fields = ['client', 'products', 'status',
                  'delivery_address', 'created_at']



class RatingReadOnlyCourierSerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField('%d-%m-%Y')
    class Meta:
        model = RatingCourier
        fields = ['courier', 'stars', 'created_date']


class RatingCourierSerializer(serializers.ModelSerializer):
    class Meta:
        model = RatingCourier
        fields = '__all__'



class CourierListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courier
        fields = ['user', 'status', 'current_orders']



class CourierDetailSerializer(serializers.ModelSerializer):
    courier = RatingReadOnlyCourierSerializer(read_only=True)
    class Meta:
        model = Courier
        fields = ['user', 'status', 'current_orders', 'courier']



class ReviewReadOnlySerializer(serializers.ModelSerializer):
    client = UserProfileSimpleSerializer(read_only=True)
    class Meta:
        model = Review
        fields = ['client', 'comment', 'rating']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'




class StoreListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    store_review = ReviewReadOnlySerializer(many=True, read_only=True)
    class Meta:
        model = Store
        fields = ['id', 'store_name', 'store_image', 'category', 'category', 'store_review']



class StoreDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    product_store = ProductListSerializer(many=True, read_only=True)
    store_combo = ProductComboListSerializer(many=True, read_only=True)
    store_contact = ContactSerializer(many=True, read_only=True)
    owner = UserProfileSimpleSerializer(read_only=True)
    client_review = ReviewReadOnlySerializer(many=True, read_only=True)
    store_review = ReviewReadOnlySerializer(many=True, read_only=True)
    class Meta:
        model = Store
        fields = ['store_name', 'owner', 'store_image', 'category',  'category', 'address',
                  'description', 'store_contact', 'product_store', 'store_combo', 'client_review', 'store_review']



class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'





