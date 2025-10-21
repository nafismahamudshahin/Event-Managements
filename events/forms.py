from django import forms
from datetime import datetime
# import model:
from events.models import Event , Category 
from events.styles import StyledFormMixin
from users.forms import StyledFormMixinextra

class CreateEventFrom(StyledFormMixinextra,forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name','description','date','time','location','image','category']
        widgets = {
            "date": forms.SelectDateWidget,
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.apply_styled_widgets()

class MakeCategoryFrom(StyledFormMixinextra,forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"

    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.apply_styled_widgets()
        
