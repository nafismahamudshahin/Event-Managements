from django import forms
from events.styles import StyledFormMixin
from events.models import Participant

class RegisterParticipantFrom(StyledFormMixin,forms.ModelForm):
    class Meta:
        model = Participant
        fields = "__all__"
        widgets = {
            "event": forms.CheckboxSelectMultiple
        }
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.apply_styled_widgets()

