
from .views import *
from django.urls import path, include
from rest_framework import routers

router = routers.SimpleRouter()

router.register(r'category', CategoryViewSet, basename='category_list')
router.register(r'order', OrderViewSet, basename='order_list')






urlpatterns = [
    path('', include(router.urls)),

    path('user/', UserProfileAPIViewView.as_view(), name='user_list'),
    path('user_profile/<int:pk>/', UserProfileEditView.as_view(), name='user_detail'),
    path('store/', StoreListAPIView.as_view(), name='store_list'),
    path('store/<int:pk>/', StoreDetailAPIView.as_view(), name='store_detail'),
    path('store/create/', StoreCreateAPIView.as_view(), name='store_create'),
    path('store_list/', StoreOwnerAPIView.as_view(), name='store_owner'),
    path('store_list/<int:pk>/', StoreEditOwnerAPIView.as_view(), name='store_edit_owner'),
    path('product/', ProductListAPIView.as_view(), name='product_list'),
    path('product_create/', ProductCreateAPIView.as_view(), name='product_create'),
    path('product_list/', ProductOwnerAPIView.as_view(), name='product_owner_list'),
    path('product_list/<int:pk>/', ProductEditOwnerAPIView.as_view(), name='product_owner_detail'),
    path('combo_list/', ProductComboListAPiView.as_view(), name='combo_list'),
    path('combo_create/', ProductComboCreateAPIView.as_view(), name='combo_create'),
    path('combo_owner/', ProductComboOwnerAPIView.as_view(), name='combo_owner_list'),
    path('combo_owner/<int:pk>/', ProductCombotEditOwnerAPIView.as_view(), name='combo_owner_detail'),
    path('rating_create/', RatingCourierCreateAPIView.as_view(), name='rating_create'),
    path('review_create/', ReviewCreateAPIView.as_view(), name='review_create'),
    path('courier/', CourierListAPIView.as_view(), name='courier_list'),
    path('courier/<int:pk>/', CourierDetailAPIView.as_view(), name='courier_detail'),
    path('cart/', CartAPIView.as_view(), name='cart_list'),
    path('cart_item/', CartItemListAPIView.as_view(), name='cart_item_list'),
    path('contact/', ContactListAPIView.as_view(), name='contact'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

]