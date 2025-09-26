from django import forms

class StyledFormMixin:
    input_classes = "w-full px-4 py-3 rounded-lg bg-zinc-900 text-white border border-neutral-700 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-rose-500 focus:border-rose-500 transition-all"
    select_classes = "w-full px-4 py-3 rounded-lg bg-zinc-900 text-white border border-neutral-700 focus:outline-none focus:ring-2 focus:ring-rose-500 focus:border-rose-500"
    checkbox_classes ="form-checkbox h-5 w-5 text-rose-500 bg-zinc-800 border-neutral-700 rounded focus:ring-rose-500"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()

    def apply_styled_widgets(self):
        for name, field in self.fields.items():
            widget = field.widget

            if isinstance(widget, (forms.TextInput, forms.EmailInput, forms.NumberInput)):
                widget.attrs.update({
                    'class': self.input_classes,
                    'placeholder': f"Enter {field.label.lower()}"
                })
            elif isinstance(widget, forms.Textarea):
                widget.attrs.update({
                    'class': f"{self.input_classes} resize-none",
                    'rows': 5,
                    'placeholder': f"Enter {field.label.lower()}"
                })
            elif isinstance(widget, forms.Select):
                widget.attrs.update({
                    'class': self.select_classes
                })
            elif isinstance(widget, forms.SelectDateWidget):
                widget.attrs.update({
                    'class': "text-white bg-zinc-900 border border-neutral-700 rounded-lg px-3 py-2"
                })
            elif isinstance(widget, forms.DateInput):
                widget.attrs.update({
                    'class': self.input_classes,
                    'type': 'date'
                })
            elif isinstance(widget, forms.TimeInput):
                widget.attrs.update({
                    'class': self.input_classes,
                    'type': 'time'
                })
            elif isinstance(widget, forms.CheckboxInput):
                widget.attrs.update({
                    'class': self.checkbox_classes
                })
            elif isinstance(widget, forms.CheckboxSelectMultiple):
                widget.attrs.update({
                    'class': "space-y-2 text-white"
                })
            elif isinstance(widget, forms.ClearableFileInput):
                widget.attrs.update({
                    'class': self.input_classes
                })
            else:
                widget.attrs.update({
                    'class': self.input_classes
                })
