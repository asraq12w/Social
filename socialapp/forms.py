from django import forms
from .models import User, Comment, Post


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=True, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=True, label="confirm Password")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'phone', 'email']

    def clean_confirm_password(self):
        cd = self.cleaned_data
        if cd['password'] != cd['confirm_password']:
            raise forms.ValidationError('password is not match with confirm password!')
        return cd['confirm_password']

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if User.objects.filter(phone=phone).exists():
            raise forms.ValidationError('phone is already exists!')
        return phone

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('email is already exists!')
        return email


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'phone', 'email', 'job', 'date_of_birth', 'photo', 'bio']

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if User.objects.exclude(id=self.instance.id).filter(phone=phone).exists():
            raise forms.ValidationError('phone is already exists!')
        return phone

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.exclude(id=self.instance.id).filter(username=username).exists():
            raise forms.ValidationError('phone is already exists!')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.exclude(id=self.instance.id).filter(email=email).exists():
            raise forms.ValidationError('phone is already exists!')
        return email


class TicketForm(forms.Form):
    SUBJECT_CHOICES = (
        ('C', 'criticism'),
        ('P', 'proposal'),
        ('R', ' report'),
    )
    subject = forms.ChoiceField(required=True, choices=SUBJECT_CHOICES)
    name = forms.CharField(required=True, max_length=100)
    phone = forms.CharField(required=True, max_length=11, min_length=11)
    email = forms.CharField(required=True, max_length=250)
    message = forms.CharField(required=True, widget=forms.Textarea())

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not phone.isnumeric():
            raise forms.ValidationError('Invalid phone number')
        return phone


class SearchForm(forms.Form):
    query = forms.CharField()


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'add-comment-text'}),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['caption', 'tags', 'image']
