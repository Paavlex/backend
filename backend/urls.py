from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from dpbackend import views
from dpbackend.views import cesta_predmetu, get_all_cards,order_card, user_register, MyTokenObtainPairView, karta_viewset,putovni_predmet_viewset

from rest_framework_simplejwt.views import (

    TokenRefreshView,
)



karta_list_retrieve = karta_viewset.as_view({'get':'retrieve'})
putovni_predmet_list_retrieve = putovni_predmet_viewset.as_view({'get':'retrieve'})

router = routers.DefaultRouter()
router.register(r'hraci', views.hrac_viewset)
router.register(r'karty', views.karta_viewset)
router.register(r'putovnipredmety', views.putovni_predmet_viewset)
router.register(r'sberpredmety', views.sberatelsky_predmet_list)



urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('cestaput/<int:vlastnik>', cesta_predmetu.as_view()),
    path('vsechnykese/', get_all_cards.as_view()),
    path('objednani/', order_card.as_view()),
    path('register/', user_register.as_view()),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('karty/<int:pk>', karta_list_retrieve),

    path('putovnipredmety/<int:pk>', putovni_predmet_list_retrieve),

    
]
