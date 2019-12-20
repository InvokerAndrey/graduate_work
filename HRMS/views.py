from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import transaction
from django.urls import reverse_lazy
from django.forms import inlineformset_factory
from django.http import HttpResponse
from django.template.loader import get_template

from .models import Employee, Education, Experience, Position, LaborCosts, Task, ForeignLanguage
from .forms import (
    EmployeeForm, 
    EducationForm, 
    ExperienceForm,
    PositionForm, 
    TaskForm, 
    LaborCostsForm, 
    PositionFilter, 
    ForeignLanguageForm
)
from .utils import render_to_pdf


def home(request):
    return render(request, 'HRMS/home.html')


def about(request):
    return render(request, 'HRMS/about.html')


def profile_method(request):
    employees = Employee.objects.filter(user=request.user)
    form = PositionFilter(request.GET)
    if form.is_valid():
        if form.cleaned_data['position']:
            employees = employees.filter(position__exact=form.cleaned_data['position'])
            raitings = estimate(employees)
            raited_employees = dict()
            for employee, raiting in zip(employees, raitings):
                raited_employees[employee] = raiting
            context = {
                'employees': employees, 
                'form': form,
                'raited_employees': raited_employees
            }
            return render(request, 'HRMS/profile_method.html', context)
    return render(request, 'HRMS/profile_method.html', {'form': form})


def estimate(employees):
    raitings = list()
    for employee in employees:
        raiting = 0
        for education in employee.education_set.all():
            raiting += 100
        for experience in employee.experience_set.all():
            raiting += 10
            exp = experience.expiration_date - experience.beginning_date
            exp = exp.days // 30
            raiting += exp
        raitings.append(raiting)
    return raitings


class EmployeeListView(LoginRequiredMixin, ListView):
    model = Employee
    template_name = 'HRMS/employees.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'employees'
    paginate_by = 3


class GeneratePDF(LoginRequiredMixin, DetailView):
    model = Employee

    def get(self, request, *args, **kwargs):
        template = get_template('HRMS/report.html')
        id_ = request.path.split('/')[2]
        employee = Employee.objects.filter(id=id_).first()
        context = {
            'employee': employee,
        }
        html = template.render(context)
        pdf = render_to_pdf('HRMS/report.html', context)
        return HttpResponse(pdf, content_type='application/pdf')

    def get_success_ul(self):
        return reverse_lazy('/')


class EmployeeDetailView(LoginRequiredMixin, DetailView):
    model = Employee

    def get_success_ul(self):
        return reverse_lazy('/')


# class TaskDetailView(LoginRequiredMixin, DetailView):
#     model = Task

#     def get_success_url(self):
#         return reverse_lazy('tasks')


class EmployeeCreateView(LoginRequiredMixin, CreateView):
    model = Employee
    fields = [
        'first_name',
        'last_name',
        'gender',
        'birthday',
        'position',
    ]

    # To define user for employee
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('employee-detail', kwargs={'pk': self.object.pk})


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = [
        'code', 
        'description', 
        'beginning_date', 
        'deadline',
    ]

    # To define user for task
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('task-detail', kwargs={'pk': self.object.pk})


class EmployeeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Employee
    fields = [
        'image',
        'first_name',
        'last_name',
        'gender',
        'birthday',
        'position',
    ]
    
    def test_func(self):
        employee = self.get_object()
        if self.request.user == employee.user:
            return True
        return False

    def get_success_url(self):
        return reverse_lazy('employee-detail', kwargs={'pk': self.object.pk})


class EmployeeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Employee

    def test_func(self):
        employee = self.get_object()
        if self.request.user == employee.user:
            return True
        return False
    
    def get_success_url(self):
        return reverse_lazy('employees')


@login_required
def update_educations(request, employee_id):
    employee = Employee.objects.get(pk=employee_id)
    EducationFormset = inlineformset_factory(
        Employee, 
        Education, 
        fields = [
            'education_type', 
            'institution_name', 
            'faculty', 
            'specialty', 
            'beginning_date', 
            'expiration_date', 
        ],
        extra=1
    )
    if request.method == 'POST':
        formset = EducationFormset(request.POST, instance=employee)
        if formset.is_valid():
            formset.save()
        return redirect('employee-detail', pk = employee.id)

    formset = EducationFormset(instance=employee)

    absolute_url = reverse_lazy('employee-detail', kwargs={'pk': employee.id})

    return render(request, 'HRMS/educations_form.html', {'formset': formset})


@login_required
def update_experiences(request, employee_id):
    employee = Employee.objects.get(pk=employee_id)
    ExperienceFormset = inlineformset_factory(
        Employee, 
        Experience, 
        fields = [
            'job',
            'beginning_date',
            'expiration_date',
            'position',
        ],
        extra=1
    )
    if request.method == 'POST':
        formset = ExperienceFormset(request.POST, instance=employee)
        if formset.is_valid():
            formset.save()
        return redirect('employee-detail', pk = employee.id)

    formset = ExperienceFormset(instance=employee)

    absolute_url = reverse_lazy('employee-detail', kwargs={'pk': employee.id})

    return render(request, 'HRMS/experiences_form.html', {'formset': formset})


@login_required
def update_tasks(request, employee_id):
    employee = Employee.objects.get(pk=employee_id)
    TaskFormset = inlineformset_factory(
        Employee, 
        Task, 
        fields = [
            'code',
            'description', 
            'beginning_date',
            'actual_expiration_date', 
            'deadline',
        ],
        extra=1
    )
    if request.method == 'POST':
        formset = TaskFormset(request.POST, instance=employee)
        if formset.is_valid():
            formset.save()
        return redirect('employee-detail', pk = employee.id)

    formset = TaskFormset(instance=employee)

    absolute_url = reverse_lazy('employee-detail', kwargs={'pk': employee.id})

    return render(request, 'HRMS/tasks_form.html', {'formset': formset})


@login_required
def update_languages(request, employee_id):
    employee = Employee.objects.get(pk=employee_id)
    TaskFormset = inlineformset_factory(
        Employee, 
        ForeignLanguage, 
        form=ForeignLanguageForm(request.GET),
        extra=1
    )
    if request.method == 'POST':
        formset = TaskFormset(request.POST, instance=employee)
        if formset.is_valid():
            formset.save()
        return redirect('employee-detail', pk = employee.id)

    formset = TaskFormset(instance=employee)

    absolute_url = reverse_lazy('employee-detail', kwargs={'pk': employee.id})

    return render(request, 'HRMS/languages_form.html', {'formset': formset})