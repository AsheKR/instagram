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

## 오류

ImageField 를 사용할 때 Image 관리를 위해 Pillow 라는 라이브러리를 사용해야한다.

Field defines a relation with model 'User', which is either not installed, or is abstract
install 되어있지 않거나, 추상 모델 'User'를 사용하고 있다.
어플리케이션을 분리했으므로 ForeignKey로 참조하는 내용을 바꿔주어야한다.
`<AppName>.<ModelName>` 로 다른 어플리케이션의 모델을 참조하거나
`from <AppName>.models import <ModelName>` 로 가져와 모델을 참조하게 해야한다.