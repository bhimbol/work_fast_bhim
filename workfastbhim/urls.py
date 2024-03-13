from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('my_profile.urls', namespace='my_profile')),
    path('asn_manager/', include('asn_manager.urls', namespace='asn_manager')),
    path('product_manager/', include('product_manager.urls', namespace='product_manager')),
    path('promo_calculator/', include('promo_calculator.urls', namespace='promo_calculator')),
    path('receive_sms/', include('sms.urls', namespace='sms')),
    path('sms/', include('sms.urls', namespace='sms')),

]





