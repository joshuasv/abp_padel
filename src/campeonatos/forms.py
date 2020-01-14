from django import forms

from crispy_forms.layout import Field, Layout
from crispy_forms.helper import FormHelper

from .models import Enfrentamiento

class EnvioEnfrentamientoForm(forms.ModelForm):
    class Meta:
        model = Enfrentamiento
        fields = ['fecha',]

    def __init__(self, *args, **kwargs):
        super(EnvioEnfrentamientoForm, self).__init__(*args, **kwargs)
        self.fields['fecha'] = forms.DateField(input_formats=['%d-%m-%Y'])
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Field('fecha', template='campeonatos/custom_date_picker.html'),
        )
