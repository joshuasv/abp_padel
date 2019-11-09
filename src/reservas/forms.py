from django import forms

from crispy_forms.layout import Field, Layout
from crispy_forms.helper import FormHelper

from .models import Reserva
from pistas.models import Pista


class ReservaCreateModelForm(forms.ModelForm):

    class Meta:
        model = Reserva
        fields = ['pista', 'hora_inicio', 'hora_fin']

    def __init__(self, *args, **kwargs):
        super(ReservaCreateModelForm, self).__init__(*args, **kwargs)
        self.fields['pista'] = forms.ModelChoiceField(queryset=Pista.objects.all())
        self.fields['hora_inicio'] = forms.DateTimeField(input_formats=['%d-%m-%Y %H:%M'])
        self.fields['hora_fin'] = forms.DateTimeField(input_formats=['%d-%m-%Y %H:%M'])

        self.fields['hora_fin'].widget.attrs['readonly'] = True

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'pista',
            Field('hora_inicio', template="reservas/custom_date_time_picker.html"),
            'hora_fin')
