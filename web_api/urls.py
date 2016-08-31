from django.conf.urls import url
from . import views

urlpatterns = [
    #/referral_system/
#    url(r'^$', views.index, name='index'),
    # ex: /referral_system/5/ referralFormOnline
    url(r'^auth/$', views.auth, name='auth'),
    url(r'^facility/$', views.getFacilities, name='getFacilities'),
    url(r'^refer/$', views.saveReferral, name='saveReferral'),
]