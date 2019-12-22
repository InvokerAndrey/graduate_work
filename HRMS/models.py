from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# from django.db.models.signals import post_save
# from django.dispatch import receiver


# Должность
class Position(models.Model):
    language_choices = [
        ('Нет', 'Нет'),
        ('Английский', 'Английский'),
        ('Немецкий', 'Немецкий'),
        ('Испанский', 'Испанский'),
        ('Китайский', 'Китайский'),
        ('Французский', 'Французский'),
    ]
    level_choices = [
        (1, 'A1'),
        (2, 'A2'),
        (3, 'B1'),
        (4, 'B2'),
        (5, 'C1'),
        (6, 'C2'),
    ]
    course_choices = [
        ('Нет', 'Нет'),
        ('Программирование', 'Программирование'),
        ('Тестирование', 'Тестирование'),
        ('Системное администрирование', 'Системное администрирование'),
        ('SAP', 'SAP'),
    ]
    education_choices = [
        (0, 'Образование не требуется'),
        (1, 'Среднее образование'),
        (2, 'Высшее образование'),
    ]
    experience_choices = [
        (0, 'Опыт работы не требуется'),
        (1, '1 год'),
        (2, '2 года'),
        (3, '3 года'),   
        (4, '4 года'),
        (5, '5 и более лет'),
    ]
    position_name = models.CharField(max_length=50, null=True)
    foreign_language = models.CharField(max_length=40, null=True, choices=language_choices)
    language_level = models.DecimalField(max_digits=3, decimal_places=0, null=True, blank=True, choices=level_choices)
    education_required = models.DecimalField(max_digits=3, decimal_places=0, null=True, choices=education_choices)
    experience_required = models.DecimalField(max_digits=3, decimal_places=0, null=True, choices=experience_choices)
    course_required = models.CharField(max_length=40, null=True, choices=course_choices)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.position_name


# Работник
class Employee(models.Model):
    gender_choices = [
        ('Мужчина', 'Мужчина'),
        ('Женщина', 'Женщина'),
    ]
    image = models.ImageField(default='emp_img.jpg', upload_to='employee_pics')
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, null=True)
    gender = models.CharField(max_length=30, null=True, choices=gender_choices)
    birthday = models.DateField(null=True)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


# Иностранные языки
class ForeignLanguage(models.Model):
    name_choices = [
        ('Английский', 'Английский'),
        ('Немецкий', 'Немецкий'),
        ('Испанский', 'Испанский'),
        ('Китайский', 'Китайский'),
        ('Французский', 'Французский'),
    ]
    level_choices = [
        (1, 'A1'),
        (2, 'A2'),
        (3, 'B1'),
        (4, 'B2'),
        (5, 'C1'),
        (6, 'C2'),
    ]
    language_name = models.CharField(max_length=30, null=True, choices=name_choices)
    level = models.DecimalField(max_digits=5, decimal_places=0, null=True, choices=level_choices)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.language_name} {self.level}'


# Курсы
class Course(models.Model):
    specialization_choices = [
        ('Программирование', 'Программирование'),
        ('Тестирование', 'Тестирование'),
        ('Системное администрирование', 'Системное администрирование'),
        ('SAP', 'SAP'),
    ]

    company = models.CharField(max_length=50, null=True)
    specialization = models.CharField(max_length=50, null=True, choices=specialization_choices)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.company}: {self.specialization}'


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
    type_choices = [
        (2, 'Высшее образование'),
        (1, 'Среднее образование'),
    ]
    education_type = models.DecimalField(max_digits=3, decimal_places=0, null=True, choices=type_choices)
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
