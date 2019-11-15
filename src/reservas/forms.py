from django import forms

from crispy_forms.layout import Field, Layout
from crispy_forms.helper import FormHelper

from .models import Reserva
from pistas.models import Pista, HorarioPista


class ReservaCreateModelForm(forms.ModelForm):

    class Meta:
        model = Reserva
        fields = ['pista', 'fecha', 'horario_pista']

    def __init__(self, *args, **kwargs):
        super(ReservaCreateModelForm, self).__init__(*args, **kwargs)
        # self.fields['pista'] = forms.ModelChoiceField(queryset=Pista.objects.all())
        self.fields['fecha'] = forms.DateField(input_formats=['%d-%m-%Y'])
        # self.fields['horario_pista'] = forms.ModelChoiceField(queryset=HorarioPista.objects.all())
        self.fields['horario_pista'] = MyModelChoiceField(queryset=HorarioPista.objects.none())
        # self.fields['horario_pista'].queryset = HorarioPista.objects.none()

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'pista',
            Field('fecha', template="reservas/custom_date_time_picker.html"),
            'horario_pista')


class MyModelChoiceField(forms.ModelChoiceField):

    def to_python(self, value):
        if self.queryset.model.DoesNotExist:
            key = self.to_field_name or 'pk'
            value = HorarioPista.objects.filter(**{key: value})
            if not value.exists():
                raise ValidationError(self.error_messages['invalid_choice'], code='invalid_choice')
            else:
                value = value.first()
        return value
