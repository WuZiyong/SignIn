from django import forms
  
'''
上传表单
'''
class UploadForm(forms.Form):
    file = forms.FileField(
    widget=forms.ClearableFileInput(attrs={'multiple': True}), # 支持多文件上传
    label='选择文件...',
    help_text='最大100M'
 )