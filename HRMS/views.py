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

from .models import Employee, Education, Experience, Position, LaborCosts, Task, ForeignLanguage, Course
from .forms import (
    EmployeeForm, 
    EducationForm, 
    ExperienceForm,
    PositionForm, 
    TaskForm, 
    LaborCostsForm, 
    PositionFilter,
)
from .utils import render_to_pdf


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
            est = estimate(employees, position)
            raitings = est[0]
            results = est[1]
            raited_employees = dict()
            for employee, raiting, result in zip(employees, raitings, results):
                raited_employees[employee] = [raiting, result]
            context = {
                'employees': employees,
                'position': position,
                'raited_employees': raited_employees,
            }
            return render(request, 'HRMS/profile_method.html', context)
    # if form.is_valid():
    #     if form.cleaned_data['position']:
    #         employees = employees.filter(position__exact=form.cleaned_data['position'])
    #         raitings = estimate(employees)
    #         raited_employees = dict()
    #         for employee, raiting in zip(employees, raitings):
    #             raited_employees[employee] = raiting
    #         context = {
    #             'employees': employees,
    #             'form': form,
    #             'raited_employees': raited_employees
    #         }
    #         return render(request, 'HRMS/profile_method.html', context)
    return render(request, 'HRMS/profile_method.html', {'form': form})


def estimate(employees, position):
    raitings = list()
    results = list()
    for employee in employees:
        suits = True
        raiting = 0
        for education in employee.education_set.all():
            if education.education_type < position.education_required:
                suits = False
            if education.education_type == 2:
                raiting += 10
            elif education.education_type == 1:
                raiting += 5
        for experience in employee.experience_set.all():
            raiting += 5
            exp = experience.expiration_date - experience.beginning_date
            exp_years = exp.days / 365
            raiting += int(exp_years * 5)
            if exp_years < position.experience_required:
                suits = False
        lang = False
        for language in employee.foreignlanguage_set.all():
            raiting += 1
            raiting += language.level
            if position.foreign_language == None:
                lang = True
            if language.language_name == position.foreign_language:
                if language.level >= position.language_level:
                    lang = True

        if not lang:
            suits = False

        for course in employee.course_set.all():
            raiting += 5

        if position.course_required == 'Нет':
            pass
        else:
            spec = False
            for course in employee.course_set.all():
                if course.specialization == position.course_required:
                    spec = True
            if not spec:
                suits = False

        raitings.append(raiting)
        results.append(suits)
    return (raitings, results)


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
        'foreign_language',
        'language_level',
        'education_required',
        'experience_required',
        'course_required',
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



class PositionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Position
    fields = [
        'position_name',
        'foreign_language',
        'language_level',
        'education_required',
        'experience_required',
        'course_required',
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
    LanguageFormset = inlineformset_factory(
        Employee,
        ForeignLanguage,
        fields = [
            'language_name',
            'level',
        ],
        extra=1
    )
    if request.method == 'POST':
        formset = LanguageFormset(request.POST, instance=employee)
        if formset.is_valid():
            formset.save()
        return redirect('employee-detail', pk = employee.id)

    formset = LanguageFormset(instance=employee)

    absolute_url = reverse_lazy('employee-detail', kwargs={'pk': employee.id})

    return render(request, 'HRMS/languages_form.html', {'formset': formset})


@login_required
def update_courses(request, employee_id):
    employee = Employee.objects.get(pk=employee_id)
    CourseFormset = inlineformset_factory(
        Employee,
        Course,
        fields = [
            'company',
            'specialization',
        ],
        extra=1
    )
    if request.method == 'POST':
        formset = CourseFormset(request.POST, instance=employee)
        if formset.is_valid():
            formset.save()
        return redirect('employee-detail', pk = employee.id)

    formset = CourseFormset(instance=employee)

    absolute_url = reverse_lazy('employee-detail', kwargs={'pk': employee.id})

    return render(request, 'HRMS/courses_form.html', {'formset': formset})