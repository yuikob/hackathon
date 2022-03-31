import json
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponse

from .models import Pochi

from .analysis_tools.hsd_tools import (
    read_HSD_from_buffer,
    HSD_to_RGB,
    RGB_to_PIL,
    PIL_to_b64,
    GetBoxSpectrum,
    get_spectrum_PIL,
)

from PIL import Image
import numpy as np
from io import BytesIO

# Create your views here.
class TestView(TemplateView):
    # HSDアップロード処理

    template_name = "test.html"

    def post(self, request, *args, **kwargs):
        """POSTリクエストに対する処理
        HSDを取得してRGBで返す
        """
        print(request)

        hsd = request.FILES.get("file", "")
        filedata = hsd.open().read()

        # hsdデータをndarrayに変換
        hsd_arr = read_HSD_from_buffer(
            filedata,
            480,
            640,
            file_extension=hsd.name.split(".")[-1],
            bit_depth=8,
        )

        print('hsd_arrのタイプ')
        print(type(hsd_arr))

        rgb_arr = HSD_to_RGB(hsd_arr)  # HSDのndarray→RGBのndarray
        rgb_pil = RGB_to_PIL(rgb_arr)  # ndarray→PIL.Image
        rgb_b64 = PIL_to_b64(rgb_pil)  # PIL.Image→b64形式str

        # セッションにデータを保存
        # ndarray形式のHSD
        request.session["hsd"] = hsd_arr
        # Pillow.Image形式のRGB画像
        request.session["rgb_pil"] = rgb_pil

        # poshiデータを登録
        pochi_obj = Pochi.objects.create(
            hsd_data=hsd,
            rgb_base64=rgb_b64,
        )

        json_res = {
            "status": "success",
            "rgb_b64": rgb_b64,
        }

        print("send json_res")

        return JsonResponse(json_res)

def get_pochi_info(request):
    rgb_obj = Pochi.objects.filter()
    
    if len(rgb_obj) == 0:
        print('Could not find rgb objects')
        return JsonResponse({"status": "failed"}, safe=False)
    elif len(rgb_obj) > 1:
        print("Multiple rgb objects has been detected.")
        return JsonResponse({"status": "failed"}, safe=False)
    else:
        rgb_obj = rgb_obj[0]

    json_res = {
        "status": "success",
        "rgb_image": rgb_obj.rgb_base64,
    }
    return JsonResponse(json_res, safe=False)


class AnnotationView(TemplateView):
    # HSDアップロード処理

    template_name = "annotation.html"

    def post(self, request, *args, **kwargs):
        #json.loadsで文字列を辞書型にデコード（変換）している
        datas = json.loads(request.body)

        pochi_obj = Pochi.objects.last()

        # DBからHSDデータを取得
        hsd = pochi_obj.hsd_data
        filedata = hsd.open().read()

        print(type(hsd), hsd.name)
        # hsdデータをndarrayに変換
        hsd_arr = read_HSD_from_buffer(
            filedata,
            480,
            640,
            file_extension=hsd.name.split(".")[-1],
            bit_depth=8,
        )

        PIL_img = get_spectrum_PIL(hsd_arr, datas["all_xy"], list(datas["color_list"]))  # PIL_imgが返ってくる

        graph_b64 = PIL_to_b64(PIL_img)  # PIL.Image（グラフ）→b64形式に変換

        json_res = {
            "status": "success",
            "graph": graph_b64,
            "message": 'できました！'
        }

        return JsonResponse(json_res)



