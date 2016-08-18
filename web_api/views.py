from datetime import datetime
from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login
from referral_system.classes.Referral import Referral
import json
from referral_system.classes.AjaxFunction import AjaxFunction
from referral_system.models import SmsFac, Client, Appointment
from django.core import serializers
from referral_system.classes.ReferralFunctions import ReferralFunctions


# Create your views here.
from web_api.classes.mSerializers import MSerializers

def getFacilities(request):
    mSerializer = MSerializers()
    facilities = mSerializer.select_all_facilities()
    appointments = mSerializer.select_all_appointments()
    services = mSerializer.select_all_services()
    return HttpResponse(
        content_type='application/json',
        content=json.dumps({
                'success': 1,
                'error_msg': "OK",
                "facilities": facilities,
                "appointments": appointments,
                "services":services
        },default=_json_serial))

def auth(request):
    username = request.POST['login']
    password = request.POST['password']
    user = authenticate(username=username, password=password)

    if user is not None:
        if user.is_active:
            login(request, user)
            mSerializer = MSerializers()
            user = mSerializer.getUser(username)

            return HttpResponse(
                content_type='application/json',
                content=json.dumps({
                        'success': 1,
                        'error_msg': "SUCCESSFUL",
                        "error_msg": "You're Logged Successfully",
                        "user": user
                },default=_json_serial))
        else:
            # Return a 'disabled account' error message
#            return redirect(loginPage, error="inactive")
            return HttpResponse(
                content_type='application/json',
                content=json.dumps({
                        'success': -1,
                        'error_msg': "ERROR_INACTIVE",
                },default=_json_serial))

    else:
        # Return an 'invalid login' error message.
#        return redirect(loginPage, error="wrong")
        return HttpResponse(
            content_type='application/json',
            content=json.dumps({
                    'success': -2,
                    'error_msg': "ERROR_WRONG",
            },default=_json_serial))


def _json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError ("Type not serializable")