import os

from django.http import FileResponse
from django.shortcuts import render

from django.conf import settings

# static() 함수로 인해 필요가 없어짐
# def media_serve(request, path):
#     # 1. /media/ 로 시작하는 모든 URL이 이 view를 통해 처리
#     # 2. /media/<추가경로>/ 에서 <추가경로> 부분을 path 에 할당
#     # 3. settings에 있는 MEDIA_ROOT 를 기준으로 <추가경로>에 해당하는 파일의 경로를 file_path 에 할당
#     #       (import 경로: django.conf import settings ) settings.MEDIA_ROOT
#     # 4. file_path 를 open 한 '파일 객체'를 FileResponse에 담아 리턴
#     #   content type 은 minetypes 라는 모듈로 동적으로 판단 가능하다.
#     #   minetypes.guess_type(경로 또느 파일 명)
#     file_path = os.path.join(settings.MEDIA_ROOT, path)
#     return FileResponse(open(file_path, 'rb'), content_type='image/jpeg')