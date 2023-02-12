from django import forms
  
# import GeeksModel from models.py
from .models import*
  
# create a ModelForm
class RecordForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = Record
        fields = "__all__"


class TrainingForm(forms.ModelForm):
    class Meta:
        model = Trainer_form
        fields = '__all__'

class BlogForm(forms.ModelForm):
    class Meta:
        model = BlogModel
        fields = ['content']        
