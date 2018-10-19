# Instagram

인스타그램 만들기

## 기능

- 포스트 (Post)
    - 작성자 (author)
    - 사진 (photo)
    - 댓글 목록
- 포스트 댓글 (Comment)
    - 해당 포스트 (post)
    - 작성자 (author)
    - 내용 (content)
    - 해시태그
    - 멘션
    
- 해시태그 (HashTag)
    - 태그명 (name)
    
- 사용자 (User)
    - 사용자 명 (username)
    - 프로필 이미지 (img_profile)
    - 이름 (name)
    - 웹사이트 (site)
    - 소개 (introduce)
    
## 화면

- 프로필
    - 내 게시물 목록
    - 내 팔로워 목록
    - 내 팔로잉 목록
- 로그인
- 포스트 피드 (포스트 리스트)
- 포스트 작성
- 포스트 디테일

## 기능

- 회원가입
- 로그인
- 포스트 작성/삭제
- 팔로우 / 언팔
- 포스트 좋아요 / 좋아요 취소
- 포스트에 댓글 작성/수정/삭제
    - 댓글 작성 시 해시태그/멘션 추가
- 해시태그 검색
- 프로필 수정

## 깨우친 사항

1. 작성 순서
    모델 -> 관리자페이지에서 정상 동작하는지 확인

0. 기타
다수(Many)인 쪽에 ForeignKey를 작성해야한다.
    One(User) : Many(Comment), One(Post) : Many(Comment)

application 이름은 복수형으로 적어주는 것이 좋다. (members, posts)

관계를 사용하는 필드 이외에 verbose_name 은 반드시 첫 인자로 사용하여야 한다.

app.py 에 verbrose_name을 작성하면 admin 페이지의 그룹 이름을 바꿀 수 있다. 하지만 변경해도 바뀌지 않는 이유는, 장고가 settings에 있는 Installed_Apps 내부에 어플리케이션을 참조할때 <AppName>Config 클래스를 참조하지 않기 때문이다.
    그렇기 때문에 settings에 InstallApp 내부에 정확히 Config 클래스를 정확히 가리키게 해야한다. `<AppFolderName>.apps.<AppName>Config` 를 리스트 내부에 적어주어야한다.
    
settings 안에 `MEDIA_ROOT` 가 존재한다면 그 폴더 하위에 upload_to 설정값에 저장되게 된다.
upload_to 를 통해 이미지를 저장했지만, Django 에서 유저가 업로드한 파일을 잘 읽지 못한다. `User Uploaded Source File` 이라고 한다. 이 파일은 소스코드 내부(git)에 포함되면 안된다. 이 파일을 읽기 위해서는 `MEDIA_URL` 을 사용하여야 한다.
`config.urls`를 참고하려고 하기때문에 아직까지 이미지를 불러오지 못한다. 그러므로 `config.urls`에 url을 지정하고, view를 작성한다. 이 과정은 static(prefix, document_root) 함수로 한번에 처리할 수 있다.
> settgins.MEDIA_URL 로 시작하는 요청은 settings.MEDIA_ROOT에서 파일을 검색하고 있으면 해당 파일을 Response
> /static/ (settings.STATIC_URL) 으로 시작하는 요청은 STATICSFILES_DIRS 리스트 파일목록을 검색, 있으면 해당 파일을 response

URLConf 를 사용할 때 `<path:<name>>` 은 `/`를 포함한 경로를 탐색한다. 즉, 해당 위치부터 주소의 끝까지를 의미하는 것 같다.

STATIC과 MEDIA의 차이는, 서버의 정적파일이냐, 유저의 정적 파일이냐의 차이. 서버의 정적파일은 소스코드(git)에 포함되어 있어야하고, 유저의 정적 파일은 소스코드(git)에 포함될 필요가 없다.

Normalize.css를 사용하면 브라우저 별 CSS 기본사항을 맞추어준다.


## 오류

ImageField 를 사용할 때 Image 관리를 위해 Pillow 라는 라이브러리를 사용해야한다.

Field defines a relation with model 'User', which is either not installed, or is abstract
install 되어있지 않거나, 추상 모델 'User'를 사용하고 있다.
어플리케이션을 분리했으므로 ForeignKey로 참조하는 내용을 바꿔주어야한다.
`<AppName>.<ModelName>` 로 다른 어플리케이션의 모델을 참조하거나
`from <AppName>.models import <ModelName>` 로 가져와 모델을 참조하게 해야한다.