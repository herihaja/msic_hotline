from django.conf.urls import url
from . import views

urlpatterns = [
    #/referral_system/
    url(r'^$', views.index, name='index'),
    # ex: /referral_system/5/ referralFormOnline
    url(r'^(?P<client_id>[0-9]+)/$', views.viewClient, name='viewClient'),
    
    #/referral_online/
    url(r'^online/', views.referralFormOnline, name='referralFormOnline'),
    #url(r'^online/(?P<notifi>.+)/$', views.referralFormOnline, name='referralFormOnline'),
    url(r'^existing/', views.referralFormExisting, name='referralFormExisting'),
    url(r'^loginPage/$', views.loginPage, name='loginPage'),
    url(r'^loginPage/(?P<error>.+)/$', views.loginPage, name='loginPage'),
    url(r'^authenticateMsicHotline/', views.authenticateMsicHotline, name='authenticateMsicHotline'),    
    url(r'^referralSaveOnlineForm/$', views.referralSaveOnlineForm, name='referralSaveOnlineForm'),
    url(r'^referralSaveExistingForm/$', views.referralSaveExistingForm, name='referralSaveExistingForm'),   
    
     
    url(r'^notificationPage/(?P<typenotif>[0-9]{2})/$', views.notificationPage, name='notificationPage'),
    
    url(r'^logout/$', 'django.contrib.auth.views.logout',{'next_page': '/referral_system/loginPage/logout'}),
    #ajax url
    url(r'^ajaxListDistrict/$', views.ajaxListDistrict, name='ajaxListDistrict'),
    url(r'^ajaxListVillage/$', views.ajaxListVillage, name='ajaxListVillage'),
    url(r'^ajaxListFacilities/$', views.ajaxListFacilities, name='ajaxListFacilities'),
    url(r'^ajaxSelectFacility/$', views.ajaxSelectFacility, name='ajaxSelectFacility'),    
    url(r'^ajaxListGFDistrict/$', views.ajaxListGFDistrict, name='ajaxListGFDistrict'),
    url(r'^ajaxListGFVillage/$', views.ajaxListGFVillage, name='ajaxListGFVillage'),
    url(r'^ajaxListGarment/$', views.ajaxListGarment, name='ajaxListGarment'),
    
    
    
    
    
]
    