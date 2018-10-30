import imghdr

import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile


User = get_user_model()


class FacebookBackend:
    def authenticate(self, request, facebook_request_token):
        api_base = 'https://graph.facebook.com/v3.2'

        api_get_access_token = f'{api_base}/oauth/access_token'
        api_me_user = f'{api_base}/me'

        # requestToken
        code = request.GET.get('code')
        # settings를 가져올 때는 django.conf.settings
        # django.conf.settings 는 lazy한 처리를 할기때문에 config.settings를 사용하는것은 좋지 않다.
        client_id = settings.FACEBOOK_APP_ID
        redirect_uri = 'http://localhost:8000/members/facebook_login'
        client_secret = settings.FACEBOOK_APP_SECRET

        params = {
            'client_id': client_id,
            'redirect_uri': redirect_uri,
            'client_secret': client_secret,
            'code': code
        }

        # requestToken to AccessToken
        response = requests.get(api_get_access_token, params)

        # Json To Python Object
        # response_object = json.loads(response.text)
        data = response.json()
        access_token = data.get('access_token')

        # AccessToken을 사용하여 사용자정보 가져오기
        params = {
            'access_token': access_token,
            'fields': ','.join([
                'id',
                'first_name',
                'last_name',
                'picture.type(large)',
            ]),
        }
        response = requests.get(api_me_user, params)
        data = response.json()

        facebook_id = data['id']
        first_name = data['first_name']
        last_name = data['last_name']
        url_img_profile = data['picture']['data']['url']

        # 응답의 bynary dat를 사용해서 In-memotry binary stream(file) 객체를 생성
        # img_response = requests.get(url_img_profile)
        # f = io.Bytes.IO(img_response.content)

        img_response = requests.get(url_img_profile)
        # imghdr을 이용해 Image binary data의 확장자를 알아냄
        img_extensions = imghdr.what('', h=img_response.content)
        # form에서 업로드한 것과 같은 형태의 file-like object를 생성
        # 첫 인수로 파일명, <facebook_id>.<확장자>형태의 파일을 지정
        # request.FILES 안쪽의 파일객체들이 InMemoryUploadedFile 형태를 가지고 있고, 객체 저장시 upload_to에 자동으로 저장한다.
        # SimpleUploadedFile은 InMemotryUploadedFile을 상속받는다.
        binary_img = SimpleUploadedFile(f'{facebook_id}.{img_extensions}', img_response.content)

        # User객체가 다른것과는 달리 create_user가 있는경우 password를 암호화해주는 로직이 있기 때문이다.
        try:
            user = User.objects.get(username=facebook_id)
            # update_or_create
            user.last_name = last_name
            user.first_name = first_name
            # user.img_profile = binary_img
            user.save()
        except User.DoesNotExist:
            user = User.objects.create_user(
                username=facebook_id,
                first_name=first_name,
                last_name=last_name,
                img_profile=binary_img,
            )
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None