from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class TemperatureForm(forms.Form):
    fuel = forms.IntegerField(help_text="Enter fuel temperature", initial=300)
    termfuel = forms.IntegerField(help_text="Enter termfuel temperature", initial=300)
    clad = forms.IntegerField(help_text="Enter clad temperature", initial=300)
    tube = forms.IntegerField(help_text="Enter tube temperature", initial=300)

    def clean_fuel(self):
        data = self.cleaned_data['fuel']
        if data > 100_000:
            raise ValidationError(_('Invalid fuel temperature > 100_000K'))
        if data < 300:
            raise ValidationError(_('Invalid fuel temperature < 300K'))
        return data

    def clean_termfuel(self):
        data = self.cleaned_data['termfuel']
        if data > 100_000:
            raise ValidationError(_('Invalid termfuel temperature > 100_000K'))
        if data < 300:
            raise ValidationError(_('Invalid termfuel temperature < 300K'))
        return data

    def clean_clad(self):
        data = self.cleaned_data['clad']
        if data > 100_000:
            raise ValidationError(_('Invalid clad temperature > 100_000K'))
        if data < 300:
            raise ValidationError(_('Invalid clad temperature < 300K'))
        return data

    def clean_tube(self):
        data = self.cleaned_data['tube']
        if data > 100_000:
            raise ValidationError(_('Invalid tube temperature > 100_000K'))
        if data < 300:
            raise ValidationError(_('Invalid tube temperature < 300K'))
        return data


class PinsForm(forms.Form):
    pin1_void1 = forms.FloatField(help_text="Enter radius for PIN1 void")
    pin1_fuel = forms.FloatField(help_text="Enter radius for PIN1 fuel")
    pin1_void2 = forms.FloatField(help_text="Enter radius for PIN1 void")
    pin1_clad= forms.FloatField(help_text="Enter radius for PIN1 clad")

    pin2_termfuel = forms.FloatField(help_text="Enter radius for PIN2 termfuel")
    pin2_clad = forms.FloatField(help_text="Enter radius for PIN2 clad")

    def clean_pin1_void1(self):
        data = self.cleaned_data['pin1_void1']
        if data < 0:
            raise ValidationError(_('Invalid radius PIN1 void < 0'))
        return data

    def clean_pin1_fuel(self):
        data = self.cleaned_data['pin1_fuel']
        if data < 0:
            raise ValidationError(_('Invalid radius PIN1 fuel < 0'))
        return data

    def clean_pin1_void2(self):
        data = self.cleaned_data['pin1_void2']
        if data < 0:
            raise ValidationError(_('Invalid radius PIN1 void < 0'))
        return data

    def clean_pin1_clad(self):
        data = self.cleaned_data['pin1_clad']
        if data < 0:
            raise ValidationError(_('Invalid radius PIN1 clad < 0'))
        return data

    def clean_pin2_termfuel(self):
        data = self.cleaned_data['pin2_termfuel']
        if data < 0:
            raise ValidationError(_('Invalid radius PIN2 termfuel < 0'))
        return data

    def clean_pin2_clad(self):
        data = self.cleaned_data['pin2_clad']
        if data < 0:
            raise ValidationError(_('Invalid radius PIN2 clad < 0'))
        return data


class ZonesForm(forms.Form):
    zone1_x = forms.FloatField(help_text="Enter zone1 x0", initial=0.0)
    zone1_y = forms.FloatField(help_text="Enter zone1 y0", initial=0.0)
    zone1_d = forms.FloatField(help_text="Enter zone1 d", initial=0.44)

    zone2_x = forms.FloatField(help_text="Enter zone2 x0", initial=0.0)
    zone2_y = forms.FloatField(help_text="Enter zone2 y0", initial=0.0)
    zone2_d = forms.FloatField(help_text="Enter zone2 d", initial=7.1)

    zone3_x = forms.FloatField(help_text="Enter zone3 x0", initial=0.0)
    zone3_y = forms.FloatField(help_text="Enter zone3 y0", initial=0.0)
    zone3_d = forms.FloatField(help_text="Enter zone3 d", initial=7.25)

    zone4_x = forms.FloatField(help_text="Enter zone4 x0", initial=0.0)
    zone4_y = forms.FloatField(help_text="Enter zone4 y0", initial=0.0)
    zone4_d = forms.FloatField(help_text="Enter zone4 d", initial=7.35)

    def clean_zone1_x(self):
        data = self.cleaned_data['zone1_x']
        if data < 0:
            raise ValidationError(_('Invalid: zone1 x0 < 0'))
        return data

    def clean_zone1_y(self):
        data = self.cleaned_data['zone1_y']
        if data < 0:
            raise ValidationError(_('Invalid: zone1 y0 < 0'))
        return data

    def clean_zone1_d(self):
        data = self.cleaned_data['zone1_d']
        if data < 0:
            raise ValidationError(_('Invalid: zone1 d < 0'))
        return data

    def clean_zone2_x(self):
        data = self.cleaned_data['zone2_x']
        if data < 0:
            raise ValidationError(_('Invalid: zone2 x0 < 0'))
        return data

    def clean_zone2_y(self):
        data = self.cleaned_data['zone2_y']
        if data < 0:
            raise ValidationError(_('Invalid: zone2 y0 < 0'))
        return data

    def clean_zone2_d(self):
        data = self.cleaned_data['zone2_d']
        if data < 0:
            raise ValidationError(_('Invalid: zone2 d < 0'))
        return data

    def clean_zone3_x(self):
        data = self.cleaned_data['zone3_x']
        if data < 0:
            raise ValidationError(_('Invalid: zone3 x0 < 0'))
        return data

    def clean_zone3_y(self):
        data = self.cleaned_data['zone3_y']
        if data < 0:
            raise ValidationError(_('Invalid: zone3 y0 < 0'))
        return data

    def clean_zone3_d(self):
        data = self.cleaned_data['zone3_d']
        if data < 0:
            raise ValidationError(_('Invalid: zone3 d < 0'))
        return data

    def clean_zone4_x(self):
        data = self.cleaned_data['zone4_x']
        if data < 0:
            raise ValidationError(_('Invalid: zone4 x0 < 0'))
        return data

    def clean_zone4_y(self):
        data = self.cleaned_data['zone4_y']
        if data < 0:
            raise ValidationError(_('Invalid: zone4 y0 < 0'))
        return data

    def clean_zone4_d(self):
        data = self.cleaned_data['zone4_d']
        if data < 0:
            raise ValidationError(_('Invalid: zone4 d < 0'))
        return data



