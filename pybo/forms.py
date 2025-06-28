from django import forms

class ScraperForm(forms.Form):
    url = forms.URLField(label='웹사이트 URL')
    tag = forms.CharField(label='HTML 태그')
    class_name = forms.CharField(label='클래스 이름', required=False)