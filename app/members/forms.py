from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.forms.utils import ErrorList

# 이를 사용하면 CustomUserModel이건 기본제공 User모델이건 신경쓰지 않아도 된다.
# 1. 사용자 모델 클래스에 대한 참조가 필요할 때
#       settings.AUTH_USER_MODEL의 값을 사용해서 사용자 모델 클래스를 반환
# 2. 사용자 모델 클래스에 대한 설정을 할 때
#       관계필드(ForeignKey, ManyToMany, OneToOne)의 관계 부분에
#       settings.AUTH_USER_MODEL(문자열)을 사용
User = get_user_model()


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # form 인스턴스가 올바르면
        # Authenticate에서 리턴된 User 객체를 채울 속성
        self._user = None

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        ),
    )

    def clean(self):
        super().clean()
        user = authenticate(username=self.cleaned_data['username'], password=self.cleaned_data['password'])
        if user is None:
            raise forms.ValidationError('해당 사용자가 없습니다!')
        self._user = user

    @property
    def user(self):
        if self.errors:
            raise ValueError('폼의 데이터 유효성 검증에 실패하였습니다.')
        return self._user


class SignupForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        ),
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        ),
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        ),
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(f"{username}가 이미 존재합니다!")

        return username

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError("패스워드가 일치하지 않습니다!")

    def save(self):
        if self.errors:
            raise ValueError('폼 데이터 유효성 검증에 실패했습니다.')
        return User.objects.create_user(username=self.cleaned_data.get('username'),
                                        password=self.cleaned_data.get('password1'))


class DivErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self: return ''
        str = ''.join(['<div class="alert alert-primary" role="alert">%s</div>' % e for e in self])
        return str
