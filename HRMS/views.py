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

from .models import Employee, Position, Task, Requirement, Skill
from .forms import EmployeeForm, PositionForm, TaskForm,  PositionFilter
from .utils import render_to_pdf
import HRMS.estimate as estimate


def home(request):
    return render(request, 'HRMS/home.html')


def about(request):
    return render(request, 'HRMS/about.html')


def profile_method(request):
    employees = Employee.objects.filter(user=request.user)
    positions = Position.objects.filter(user=request.user)
    form = PositionFilter(request.GET)
    if form.is_valid():
        if form.cleaned_data['position']:
            employees = employees.filter(position__exact=None)
            position = positions.filter(position_name__exact=form.cleaned_data['position']).first()
            estimate_result = estimate.get_estimated_employees(employees, position)
            estimated_employees = estimate_result[0]
            best_employees = estimate_result[1]
            index_range = range(1, len(estimated_employees) + 2)
            skills_grades = estimate.get_skills_grades(employees)
            requirement_grade = estimate.get_requirement_grade(position)
            context = {
                'employees': employees,
                'position': position,
                'estimated_employees': estimated_employees,
                'best_employees': best_employees,
                'index_range': index_range,
                'skills_grades': skills_grades,
                'requirement_grade': requirement_grade,
            }
            return render(request, 'HRMS/estimated_employees.html', context)
    return render(request, 'HRMS/profile_method.html', {'form': form})


class EmployeeListView(LoginRequiredMixin, ListView):
    model = Employee
    template_name = 'HRMS/employees.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'employees'
    paginate_by = 3


class PositionListView(LoginRequiredMixin, ListView):
    model = Position
    template_name = 'HRMS/positions.html'
    context_object_name = 'positions'


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


class PositionDetailView(LoginRequiredMixin, DetailView):
    model = Position

    def get_success_url(self):
        return reverse_lazy('/')


class EmployeeCreateView(LoginRequiredMixin, CreateView):
    model = Employee
    fields = [
        'first_name',
        'last_name',
        'gender',
        'birthday',
    ]

    # To define user for employee
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('employee-detail', kwargs={'pk': self.object.pk})

    
class PositionCreateView(LoginRequiredMixin, CreateView):
    model = Position
    fields = [
        'position_name',
        'education',
        'experience',
    ]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('position-detail', kwargs={'pk': self.object.pk})


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


class EmployeeEducationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Employee
    fields = [
        'education'
    ]
    
    def test_func(self):
        employee = self.get_object()
        if self.request.user == employee.user:
            return True
        return False

    def get_success_url(self):
        return reverse_lazy('employee-detail', kwargs={'pk': self.object.pk})


class EmployeeExperienceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Employee
    fields = [
        'experience'
    ]
    
    def test_func(self):
        employee = self.get_object()
        if self.request.user == employee.user:
            return True
        return False

    def get_success_url(self):
        return reverse_lazy('employee-detail', kwargs={'pk': self.object.pk})


class PositionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Position
    fields = [
        'position_name',
        'education',
        'experience',
    ]
    
    def test_func(self):
        position = self.get_object()
        if self.request.user == position.user:
            return True
        return False
    
    def get_success_url(self):
        return reverse_lazy('position-detail', kwargs={'pk': self.object.pk})


class EmployeeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Employee

    def test_func(self):
        employee = self.get_object()
        if self.request.user == employee.user:
            return True
        return False
    
    def get_success_url(self):
        return reverse_lazy('employees')


class PositionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Position

    def test_func(self):
        position = self.get_object()
        if self.request.user == position.user:
            return True
        return False

    def get_success_url(self):
        return reverse_lazy('positions')


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
def update_skills(request, employee_id):
    employee = Employee.objects.get(pk=employee_id)
    TaskFormset = inlineformset_factory(
        Employee, 
        Skill, 
        fields = [
            'skill_name',
            'value',
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

    return render(request, 'HRMS/skills_form.html', {'formset': formset})


@login_required
def update_requirements(request, position_id):
    position = Position.objects.get(pk=position_id)
    TaskFormset = inlineformset_factory(
        Position, 
        Requirement, 
        fields = [
            'requirement_name',
            'value',
        ],
        extra=1
    )
    if request.method == 'POST':
        formset = TaskFormset(request.POST, instance=position)
        if formset.is_valid():
            formset.save()
        return redirect('position-detail', pk = position.id)

    formset = TaskFormset(instance=position)

    absolute_url = reverse_lazy('position-detail', kwargs={'pk': position.id})

    return render(request, 'HRMS/requirements_form.html', {'formset': formset})


class PersonalityUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Employee
    fields = [
        'sociability',
        'smart',
        'emotionality',
        'self_centeredness',
        'tension',
    ]
    
    def test_func(self):
        employee = self.get_object()
        if self.request.user == employee.user:
            return True
        return False

    def get_success_url(self):
        return reverse_lazy('employee-detail', kwargs={'pk': self.object.pk})


class AppearanceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Employee
    fields = [
        'attractiveness',
    ]
    
    def test_func(self):
        employee = self.get_object()
        if self.request.user == employee.user:
            return True
        return False

    def get_success_url(self):
        return reverse_lazy('employee-detail', kwargs={'pk': self.object.pk})


class PositionPersonalUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Position
    fields = [
        'sociability',
        'smart',
        'emotionality',
        'self_centeredness',
        'tension',
        'attractiveness',
    ]

    template_name = 'HRMS/position_personality_form.html'

    def test_func(self):
        employee = self.get_object()
        if self.request.user == employee.user:
            return True
        return False

    def get_success_url(self):
        return reverse_lazy('position-detail', kwargs={'pk': self.object.pk})
