from django import forms
from main.models import OriginImage
class UploadImageForm(forms.ModelForm):
    class Meta:
        model = OriginImage
        fields = ['name', 'image']

class MethodForm(forms.Form):
    method_name = forms.CharField()