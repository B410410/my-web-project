from django import forms
from .models import UserForm
from captcha.fields import CaptchaField

# 客服表單
class ContactForm(forms.ModelForm):
    captcha = CaptchaField(label='請輸入圖片中的文字')  # 新增 captcha 欄位

    class Meta:
        model = UserForm
        fields = ['name', 'city', 'is_student', 'email', 'message']

        # 使用 widgets 設定 label 和其他屬性
        labels = {
            'name': '您的姓名',
            'city': '居住城市',
            'is_student': '是否在學',
            'email': '電子郵件',
            'message': '您的意見'
        }
        
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4, 'cols': 50}),
        }
        
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    #     self.fields['name'].label = '您的姓名'
    #     self.fields['city'].label = '居住城市'
    #     self.fields['is_student'].label = '是否在學'
    #     self.fields['email'].label = '電子郵件'
    #     self.fields['message'].label = '您的意見'
    
    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 2:
            raise forms.ValidationError("姓名不能少於2個字元")
        return name

# 基本資料表單
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserForm
        fields = ['name', 'city', 'is_student', 'email', 'message']
