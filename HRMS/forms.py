from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit

from users.models import Profile
import HRMS.models as models


DATE_INPUT_FORMATS = ['%d-%m-%Y']


class PositionFilter(forms.Form):
    position = forms.ModelChoiceField(required=False, label='Position', queryset=models.Position.objects.distinct('position_name'))


class ForeignLanguageForm(forms.Form):
    name_choices = [
        'Английский',
        'Немецкий',
        'Испанский',
        'Китайский',
        'Французский',
    ]
    level_choices = [
        'A1',
        'A2',
        'B1',
        'B2',
        'C1',
        'C2',
    ]
    language_name = forms.ChoiceField(label='Язык', required=False, choices=name_choices)
    level = forms.ChoiceField(label='Уровень', required=False, choices=level_choices)


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]


class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
        ]


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['image',]


class PositionForm(ModelForm):
    class Meta:
        model = models.Position
        fields = ['position_name']

class TaskForm(ModelForm):
    class Meta:
        model = models.Task
        fields = [
            'code',
            'description', 
            'beginning_date',
            'actual_expiration_date', 
            'deadline',
        ]
        # localized_fields = ('beginning_date', 'actual_expiration_date', 'deadline')


class EmployeeForm(ModelForm):
    class Meta:
        model = models.Employee
        fields = [
            'first_name',
            'last_name',
            'gender',
            'birthday',
            'position',
        ]
        localized_fields = ('birthday',)


class EmployeeUpdateForm(ModelForm):
    class Meta:
        model = models.Employee
        fields = [
            'image',
            'first_name',
            'last_name',
            'gender',
            'birthday',
            'position',
        ]
        localized_fields = ('birthday',)


class EducationForm(ModelForm):
    class Meta:
        model = models.Education
        fields = [
            'education_type', 
            'institution_name', 
            'faculty', 
            'specialty', 
            'beginning_date', 
            'expiration_date', 
        ]
        # localized_fields = ('beginning_date', 'expiration_date',)


class ExperienceForm(ModelForm):
    class Meta:
        model = models.Experience
        fields = [
            'job',
            'beginning_date',
            'expiration_date',
            'position',
        ]
        # localized_fields = ('beginning_date', 'expiration_date',)


class LaborCostsForm(ModelForm):
    class Meta:
        model = models.LaborCosts
        fields = [
            'spent_hours',
        ]
