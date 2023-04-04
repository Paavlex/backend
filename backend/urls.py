from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from dpbackend import views
from dpbackend.views import cesta_predmetu, get_all_cards,order_card,open_cache,item_upload ,user_register, MyTokenObtainPairView, karta_viewset,putovni_predmet_viewset,card_detail,card_info, get_all_cards_andoid,put_predmet_pozice

from rest_framework_simplejwt.views import (

    TokenRefreshView,
)



karta_list_retrieve = karta_viewset.as_view({'get':'retrieve'})
putovni_predmet_list_retrieve = putovni_predmet_viewset.as_view({'get':'retrieve'})

# vytovření cest pro třídy ModelViewSet
router = routers.DefaultRouter()
router.register(r'hraci', views.hrac_viewset)
router.register(r'karty', views.karta_viewset)
router.register(r'putovnipredmety', views.putovni_predmet_viewset)
#router.register(r'sberpredmety', views.sberatelsky_predmet_list)


# Vytovoření cest pro API
urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('cestaput/', cesta_predmetu.as_view()),
    path('vsechnykese/', get_all_cards.as_view()),
    path('objednani/', order_card.as_view()),
    path('register/', user_register.as_view()),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('karty/<int:pk>', karta_list_retrieve),
    path('detail-karty/<int:id>', card_detail.as_view()),
    path('info-karty/', card_info.as_view()),
    path('vsechnykeseandroid/',get_all_cards_andoid.as_view()),
    path('jeden-predmet/<int:pk>',put_predmet_pozice.as_view()),
    path('upload/', item_upload.as_view()),
    path('game/',open_cache.as_view()),
    path('putovnipredmety/<int:pk>', putovni_predmet_list_retrieve),

    
]
