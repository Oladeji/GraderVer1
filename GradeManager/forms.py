from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model ,logout,login


User = get_user_model()
class UserLoginForm(forms.Form ):
   username  = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder':'Enter Username' ,'class': 'input-line full-width'}))
   password  = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'placeholder':'Enter Password' ,'class': 'input-line full-width'}))


   def clean(self, *args ,**kwargs):
       username = self.cleaned_data.get('username')
       password = self.cleaned_data.get('password')

       if username and password :
           user = authenticate(username=username, password=password)
           if not user :
               raise forms.ValidationError('This user does not exist')
           if not user.check_password(password):
                  raise forms.ValidationError('In Correct password')
           if not user.is_active:
                  raise forms.ValidationError('This user is not active')
       return  super(UserLoginForm,self).clean(*args ,**kwargs)



class UserRegisterForm(forms.ModelForm):
    email = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder':'Enter Email' ,'class': 'input-line full-width'}))
    email2 = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder':'Confirm E mail' ,'class': 'input-line full-width'}))
    username  = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder':'Enter Username' ,'class': 'input-line full-width'}))
    password  = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'placeholder':'Enter Password' ,'class': 'input-line full-width'}))


    class Meta:
        model = User
        fields=[
            'username',
            'email',
            'email2',
            'password'
        ]


    def clean(self, *args ,**kwargs):
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')
        if email != email2:
            print(email)
            print(email2)
            raise forms.ValidationError('emails must match')
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError('This email already exists')
        return  super(UserRegisterForm,self).clean(*args ,**kwargs)
