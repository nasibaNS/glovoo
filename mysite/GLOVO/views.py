from rest_framework import viewsets, generics, status, permissions
from .models import *
from .serializers import *
from .permissions import CheckOwner, CheckOwnerEdit, CheckClient
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    serializer_class = CartSerializer
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)






class UserProfileAPIViewView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSimpleSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(username=self.request.user.username)

class UserProfileEditView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class StoreListAPIView(generics.ListAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['category']
    search_fields = ['store_name']


class StoreDetailAPIView(generics.RetrieveAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreDetailSerializer

class StoreCreateAPIView(generics.CreateAPIView):
    serializer_class = StoreSerializer
    permission_classes = [CheckOwner]

class StoreOwnerAPIView(generics.ListAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreListSerializer
    permission_classes = [CheckOwner]

    def get_queryset(self):
        return Store.objects.filter(owner__id=self.request.user.id)

class StoreEditOwnerAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [CheckOwner, CheckOwnerEdit]




class ContactListAPIView(generics.ListAPIView):
    queryset = Store.objects.all()
    serializer_class = ContactSerializer


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer


class ProductCreateAPIView(generics.CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [CheckOwner]

class ProductOwnerAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer

    def get_queryset(self):
        return Product.objects.filter(owner__id=self.request.user.id)

class ProductEditOwnerAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer



class ProductComboListAPiView(generics.ListAPIView):
    queryset = ProductCombo .objects.all()
    serializer_class = ProductComboListSerializer


class ProductComboCreateAPIView(generics.CreateAPIView):
    serializer_class = ProductComboSerializer
    permission_classes = [CheckOwner]

class ProductComboOwnerAPIView(generics.ListAPIView):
    queryset = ProductCombo.objects.all()
    serializer_class = ProductComboListSerializer

    def get_queryset(self):
        return ProductCombo.objects.filter(owner__id=self.request.user.id)

class ProductCombotEditOwnerAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductComboSerializer




class CartAPIView(generics.ListAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartItemListAPIView(generics.ListAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)



class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class CourierListAPIView(generics.ListAPIView):
    queryset = Courier.objects.all()
    serializer_class = CourierListSerializer

class CourierDetailAPIView(generics.ListAPIView):
    queryset = Courier.objects.all()
    serializer_class = CourierDetailSerializer


class RatingCourierCreateAPIView(generics.ListCreateAPIView):
    serializer_class = RatingCourierSerializer
    permission_classes = [CheckClient]


class ReviewCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [CheckClient]


