from django import forms  
class DatasetForm(forms.Form):  
    file1 = forms.FileField()