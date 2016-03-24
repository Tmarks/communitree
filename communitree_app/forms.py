from django import forms


class FaceForm(forms.Form):
    face = forms.CharField(label="Face", max_length=100)
