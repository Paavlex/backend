from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from dpbackend import views
from dpbackend.views import cesta_predmetu, get_all_cards,order_card, user_register, MyTokenObtainPairView

from rest_framework_simplejwt.views import (

    TokenRefreshView,
)





router = routers.DefaultRouter()
router.register(r'hraci', views.hrac_list)
router.register(r'karty', views.karta_list)
router.register(r'putovnipredmety', views.putovni_predmet_list)
router.register(r'sberpredmety', views.sberatelsky_predmet_list)



urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('cestaput/<str:vlastnik>', cesta_predmetu.as_view()),
    path('vsechnykese/', get_all_cards.as_view()),
    path('objednani/', order_card.as_view()),
    path('register/', user_register.as_view()),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    
]
