from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# from django.db.models.signals import post_save
# from django.dispatch import receiver


# Должность
class Position(models.Model):
    position_name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.position_name


# Работник
class Employee(models.Model):
    image = models.ImageField(default='emp_img.jpg', upload_to='employee_pics')
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, null=True)
    gender = models.CharField(max_length=30, null=True)
    birthday = models.DateField(null=True)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


# Иностранные языки
class ForeignLanguage(models.Model):
    language_name = models.CharField(max_length=30, null=True)
    level = models.CharField(max_length=10, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)


# Курсы
class Course(models.Model):
    company = models.CharField(max_length=50, null=True)
    specialization = models.CharField(max_length=50, null=True)


# Задача
class Task(models.Model):
    code = models.CharField(max_length=10, null=True)
    description = models.TextField(null=True)
    beginning_date = models.DateField(null=True)
    actual_expiration_date = models.DateField(blank=True)
    deadline = models.DateField(null=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        task = f'Code: {self.code}, description: {self.description}'
        return task


# Опыт работы
class Experience(models.Model):
    job = models.CharField(max_length=100, null=True)
    beginning_date = models.DateField(null=True)
    expiration_date = models.DateField(null=True)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return self.job


# Образование
class Education(models.Model):
    education_type = models.CharField(max_length=100, null=True)
    institution_name = models.CharField(max_length=100, null=True)
    faculty = models.CharField(max_length=100, null=True)
    specialty = models.CharField(max_length=100, null=True)
    beginning_date = models.DateField(null=True)
    expiration_date = models.DateField(null=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.institution_name}, {self.beginning_date} - {self.expiration_date}'

    def get_absolute_url(self):
        return reverse('employees')


# Трудозатраты
class LaborCosts(models.Model):
    spent_hours = models.IntegerField(null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True)
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)

    def __str__(self):
        labor_costs = f'{self.task}, {self.employee}, {self.spent_hours}'
        return labor_costs

    def get_absolute_url(self):
        return reverse('employees')
