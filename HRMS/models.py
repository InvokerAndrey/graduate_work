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
    education_choices = [
        (0, 'Образование не требуется'),
        (1, 'Неполное среднее общее образование (9 классов)'),
        (2, 'Среднее общее образование (11 классов)'),
        (3, 'Среднее специальное образование'),
        (4, 'Высшее образование (бакалавр)'),
        (5, 'Высшее образование (магистр)'),
        (6, 'Высшее образование (докторантура)'),
    ]
    experience_choices = [
        (1, 'Опыт работы не требуется'),
        (2, '1 год'),
        (3, '2 года'),
        (4, '3 года'),   
        (5, '4 года'),
        (6, '5 и более лет'),
    ]

    position_name = models.CharField(max_length=50, null=True, verbose_name=u'Название должности')
    foreign_language = models.CharField(max_length=40, null=True, choices=language_choices, verbose_name=u'Иностранный язык')
    language_level = models.DecimalField(max_digits=3, decimal_places=0, null=True, blank=True, choices=level_choices, verbose_name=u'Уровень знания языка')
    education_required = models.DecimalField(max_digits=3, decimal_places=0, null=True, choices=education_choices, verbose_name=u'Образование')
    experience_required = models.DecimalField(max_digits=3, decimal_places=0, null=True, choices=experience_choices, verbose_name=u'Опыт работы')

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    range_choices = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
    ]

    # замкнутость - общительность
    sociability = models.DecimalField(
        max_digits=3, 
        decimal_places=0, 
        null=True, blank=True, 
        choices=range_choices, 
        verbose_name=u'1 - Замкнутый, 7 - общительный'
    )
    # менее сообразительный - более сообразительный
    smart = models.DecimalField(
        max_digits=3, 
        decimal_places=0, 
        null=True, 
        blank=True, 
        choices=range_choices,
        verbose_name=u'1 - Менее сообразительный, 7 - более сообразительный'
    )
    # эмоциональный - эмоционально устойчивый
    emotionality = models.DecimalField(max_digits=3, 
        decimal_places=0, 
        null=True, 
        blank=True, 
        choices=range_choices,
        verbose_name=u'1 - эмоциональный, 7 - Эмоционально устойчивый'
    )
    # ориентированный на группу - ориентированный на себя
    self_centeredness = models.DecimalField(
        max_digits=3, 
        decimal_places=0, 
        null=True, 
        blank=True, 
        choices=range_choices,
        verbose_name=u'1 - Ориентированный на группу, 7 - ориентированный на себя'
    )
    # раскованный - напряженный
    tension = models.DecimalField(
        max_digits=3, 
        decimal_places=0, 
        null=True, 
        blank=True, 
        choices=range_choices,
        verbose_name=u'1 - напряженный, 7 - Раскованный'
    )

    # Привлекательность
    attractiveness = models.DecimalField(
        max_digits=3,
        decimal_places=0,
        null=True,
        blank=True,
        choices=range_choices,
        verbose_name=u'1 - Менее привлекательный, 7 - более привлекательный'
    )

    def __str__(self):
        return self.position_name


# Работник
class Employee(models.Model):
    gender_choices = [
        ('Мужчина', 'Мужчина'),
        ('Женщина', 'Женщина'),
    ]
    personality_choices = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
    ]
    image = models.ImageField(default='emp_img.jpg', upload_to='employee_pics', verbose_name=u'Фотография сотрудника')
    first_name = models.CharField(max_length=30, null=True, verbose_name=u'Имя')
    last_name = models.CharField(max_length=30, null=True, verbose_name=u'Фамилия')
    gender = models.CharField(max_length=30, null=True, choices=gender_choices, verbose_name=u'Пол')
    birthday = models.DateField(null=True, verbose_name=u'Дата рождения')
    position = models.ForeignKey(Position, on_delete=models.CASCADE, blank=True, null=True, verbose_name=u'Должность')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    # замкнутость - общительность
    sociability = models.DecimalField(
        max_digits=3, 
        decimal_places=0, 
        null=True, blank=True, 
        choices=personality_choices, 
        verbose_name=u'1 - Замкнутый, 7 - общительный'
    )
    # менее сообразительный - более сообразительный
    smart = models.DecimalField(
        max_digits=3, 
        decimal_places=0, 
        null=True, 
        blank=True, 
        choices=personality_choices,
        verbose_name=u'1 - Менее сообразительный, 7 - более сообразительный'
    )
    # эмоциональный - эмоционально устойчивый
    emotionality = models.DecimalField(max_digits=3, 
        decimal_places=0, 
        null=True, 
        blank=True, 
        choices=personality_choices,
        verbose_name=u'1 - эмоциональный, 7 - Эмоционально устойчивый'
    )
    # ориентированный на группу - ориентированный на себя
    self_centeredness = models.DecimalField(
        max_digits=3, 
        decimal_places=0, 
        null=True, 
        blank=True, 
        choices=personality_choices,
        verbose_name=u'1 - Ориентированный на группу, 7 - ориентированный на себя'
    )
    # раскованный - напряженный
    tension = models.DecimalField(
        max_digits=3, 
        decimal_places=0, 
        null=True, 
        blank=True, 
        choices=personality_choices,
        verbose_name=u'1 - напряженный, 7 - Раскованный'
    )

    appearance_choices = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
    ]

    attractiveness = models.DecimalField(
        max_digits=3, 
        decimal_places=0, 
        null=True, 
        blank=True, 
        choices=appearance_choices,
        verbose_name=u'1 - Менее привлекательный, 7 - более привлекательный'
    )

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
    language_name = models.CharField(max_length=30, null=True, choices=name_choices, verbose_name=u'Язык')
    level = models.DecimalField(max_digits=5, decimal_places=0, null=True, choices=level_choices, verbose_name=u'Уровень знания языка')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.language_name} {self.level}'


# Задача
class Task(models.Model):
    code = models.CharField(max_length=10, null=True, verbose_name=u'Код задачи')
    description = models.TextField(null=True, verbose_name=u'Описание')
    beginning_date = models.DateField(null=True, verbose_name=u'Дата начала')
    actual_expiration_date = models.DateField(blank=True, verbose_name=u'Дата фактического завершения')
    deadline = models.DateField(null=True, verbose_name=u'Крайний срок')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        task = f'Code: {self.code}, description: {self.description}'
        return task


# Опыт работы
class Experience(models.Model):
    job = models.CharField(max_length=100, null=True, verbose_name=u'Название компании')
    beginning_date = models.DateField(null=True, verbose_name=u'Дата начала работы')
    expiration_date = models.DateField(null=True, verbose_name=u'Дата увольнения')
    position = models.ForeignKey(Position, on_delete=models.CASCADE, verbose_name=u'должность')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return self.job


# Образование
class Education(models.Model):
    type_choices = [
        (1, 'Неполное среднее общее образование (9 классов)'),
        (2, 'Среднее общее образование (11 классов)'),
        (3, 'Среднее специальное образование'),
        (4, 'Высшее образование (бакалавр)'),
        (5, 'Высшее образование (магистр)'),
        (6, 'Высшее образование (докторантура)'),
    ]
    education_type = models.DecimalField(max_digits=3, decimal_places=0, null=True, choices=type_choices, verbose_name=u'Тип образования', default=0)
    institution_name = models.CharField(max_length=100, null=True, verbose_name=u'Название учебного заведения')
    faculty = models.CharField(max_length=100, null=True, verbose_name=u'Факультет')
    specialty = models.CharField(max_length=100, null=True, verbose_name=u'Специальность')
    beginning_date = models.DateField(null=True, verbose_name=u'Дата поступления')
    expiration_date = models.DateField(null=True, verbose_name=u'Дата окончания')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.institution_name}, {self.beginning_date} - {self.expiration_date}'

    def get_absolute_url(self):
        return reverse('employees')
