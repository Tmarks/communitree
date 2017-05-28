from django import forms


#class FaceForm(forms.Form):
#    face = forms.CharField(label="Face", max_length=100)


class PruningForm(forms.Form):
    completion_percentage = forms.DecimalField(label="Estimate how much of the pruning was done:")
