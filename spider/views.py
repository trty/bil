from django.shortcuts import render
import requests
import json
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from .view_data import *
from .models import *


class Add(View):
    def get(self, request):
        bvid = request.GET.get("bv")
        try:
            data = save_bv(bvid)
            return JsonResponse(data)
        except Exception as e:
            return JsonResponse({'success': False, 'msg': str(e)})


class Info(View):
    def get(self, request):
        bvid = request.GET.get("bv")
        bv = BvInfo.objects.filter(bvid=bvid).values()
        if bv:
            return JsonResponse({'success': True, 'data': dict(bv[0])})
        else:
            return JsonResponse({'success': False, 'msg': '没有找到此数据'})


class AddSync(View):
    def get(self, request):
        bvid = request.GET.get("bv")
        try:
            data = save_bv_sync(bvid)
            return JsonResponse(data)
        except Exception as e:
            return JsonResponse({'success': False, 'msg': str(e)})


class InfoSync(View):
    def get(self, request):
        bvid = request.GET.get("bv")
        data = cache.get(bvid)
        if data:
            return JsonResponse({'success': True, 'data': data})
        bv = BvInfo.objects.filter(bvid=bvid).values()
        if bv:
            return JsonResponse({'success': True, 'data': dict(bv[0])})
        else:
            return JsonResponse({'success': False, 'msg': '没有找到此数据'})

