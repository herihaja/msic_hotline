from django.conf.urls import url
from . import views

urlpatterns = [
    #/referral_system/
#    url(r'^$', views.index, name='index'),
    # ex: /referral_system/5/ referralFormOnline
    url(r'^$', views.myPing, name='myPing'),
    url(r'^auth/$', views.auth, name='auth'),
    url(r'^facility/$', views.getFacilities, name='getFacilities'),
    url(r'^update/$', views.getAllUpdate, name='getAllUpdate'),
    url(r'^refer/$', views.saveReferral, name='saveReferral'),
    url(r'^refer4/$', views.saveReRefer, name='saveReRefer'),
    url(r'^redeem/$', views.saveRedeem, name='saveRedeem'),
    url(r'^garment_report/$', views.updateGarmentReport, name='updateGarmentReport'),
    url(r'^reset_pass/$', views.resetPassword, name='resetPassword'),
]