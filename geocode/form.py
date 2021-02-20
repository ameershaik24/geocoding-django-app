from django import forms

class StudentForm(forms.Form):
    input_file = forms.FileField(required=True)