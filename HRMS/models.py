from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# from django.db.models.signals import post_save
# from django.dispatch import receiver


# Должность
class Position(models.Model):
    value_choices = [
        (1, '1. Кандидат не владеет навыком'),
        (2, '2. Кандидат владеет навыком недостаточно'),
        (3, '3. Навык у кандидата проявляется достаточно четко'),
        (4, '4. Навык у кандидата проявляется со средней активностью'),
        (5, '5. Кандидат хорошо владеет навыком'),
        (6, '6. Кандидат владеет навыком очень хорошо'),
        (7, '7. Кандидат владеет навыком превосходно'),
    ]

    position_name = models.CharField(max_length=50, null=True, verbose_name=u'Название должности')
    foreign_language = models.CharField(max_length=40, null=True, choices=value_choices, verbose_name=u'Иностранный язык')
    language_level = models.DecimalField(max_digits=3, decimal_places=0, null=True, blank=True, choices=value_choices, verbose_name=u'Уровень знания языка')
    education_required = models.DecimalField(max_digits=3, decimal_places=0, null=True, choices=value_choices, verbose_name=u'Образование')
    experience_required = models.DecimalField(max_digits=3, decimal_places=0, null=True, choices=value_choices, verbose_name=u'Опыт работы')

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    education = models.DecimalField(
        max_digits=3, 
        decimal_places=0, 
        null=True, 
        choices=value_choices,
        blank=True,
        verbose_name=u'Образование', 
        default=0
    )

    experience = models.DecimalField(
        max_digits=3, 
        decimal_places=0, 
        null=True, 
        choices=value_choices,
        blank=True,
        verbose_name=u'Опыт работы',
        default=0
    )

    # замкнутость - общительность
    sociability = models.DecimalField(
        max_digits=3, 
        decimal_places=0, 
        null=True, 
        blank=True, 
        choices=value_choices, 
        verbose_name=u'1 - Замкнутый, 7 - общительный'
    )
    # менее сообразительный - более сообразительный
    smart = models.DecimalField(
        max_digits=3, 
        decimal_places=0, 
        null=True, 
        blank=True, 
        choices=value_choices,
        verbose_name=u'1 - Менее сообразительный, 7 - более сообразительный'
    )
    # эмоциональный - эмоционально устойчивый
    emotionality = models.DecimalField(max_digits=3, 
        decimal_places=0, 
        null=True, 
        blank=True, 
        choices=value_choices,
        verbose_name=u'1 - эмоциональный, 7 - Эмоционально устойчивый'
    )
    # ориентированный на группу - ориентированный на себя
    self_centeredness = models.DecimalField(
        max_digits=3, 
        decimal_places=0, 
        null=True, 
        blank=True, 
        choices=value_choices,
        verbose_name=u'1 - Ориентированный на группу, 7 - ориентированный на себя'
    )
    # раскованный - напряженный
    tension = models.DecimalField(
        max_digits=3, 
        decimal_places=0, 
        null=True, 
        blank=True, 
        choices=value_choices,
        verbose_name=u'1 - напряженный, 7 - Раскованный'
    )

    # Привлекательность
    attractiveness = models.DecimalField(
        max_digits=3,
        decimal_places=0,
        null=True,
        blank=True,
        choices=value_choices,
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
    value_choices = [
        (1, '1. Кандидат не владеет навыком'),
        (2, '2. Кандидат владеет навыком недостаточно'),
        (3, '3. Навык у кандидата проявляется достаточно четко'),
        (4, '4. Навык у кандидата проявляется со средней активностью'),
        (5, '5. Кандидат хорошо владеет навыком'),
        (6, '6. Кандидат владеет навыком очень хорошо'),
        (7, '7. Кандидат владеет навыком превосходно'),
    ]
    image = models.ImageField(default='emp_img.jpg', upload_to='employee_pics', verbose_name=u'Фотография сотрудника')
    first_name = models.CharField(max_length=30, null=True, verbose_name=u'Имя')
    last_name = models.CharField(max_length=30, null=True, verbose_name=u'Фамилия')
    gender = models.CharField(max_length=30, null=True, choices=gender_choices, verbose_name=u'Пол')
    birthday = models.DateField(null=True, verbose_name=u'Дата рождения')
    position = models.ForeignKey(Position, on_delete=models.CASCADE, blank=True, null=True, verbose_name=u'Должность')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    education = models.DecimalField(
        max_digits=3, 
        decimal_places=0, 
        null=True, 
        choices=value_choices,
        blank=True,
        verbose_name=u'Образование', 
        default=0
    )

    experience = models.DecimalField(
        max_digits=3, 
        decimal_places=0, 
        null=True, 
        choices=value_choices,
        blank=True,
        verbose_name=u'Опыт работы',
        default=0
    )

    # замкнутость - общительность
    sociability = models.DecimalField(
        max_digits=3, 
        decimal_places=0, 
        null=True, blank=True, 
        choices=value_choices, 
        verbose_name=u'1 - Замкнутый, 7 - общительный'
    )
    # менее сообразительный - более сообразительный
    smart = models.DecimalField(
        max_digits=3, 
        decimal_places=0, 
        null=True, 
        blank=True, 
        choices=value_choices,
        verbose_name=u'1 - Менее сообразительный, 7 - более сообразительный'
    )
    # эмоциональный - эмоционально устойчивый
    emotionality = models.DecimalField(max_digits=3, 
        decimal_places=0, 
        null=True, 
        blank=True, 
        choices=value_choices,
        verbose_name=u'1 - эмоциональный, 7 - Эмоционально устойчивый'
    )
    # ориентированный на группу - ориентированный на себя
    self_centeredness = models.DecimalField(
        max_digits=3, 
        decimal_places=0, 
        null=True, 
        blank=True, 
        choices=value_choices,
        verbose_name=u'1 - Ориентированный на группу, 7 - ориентированный на себя'
    )
    # раскованный - напряженный
    tension = models.DecimalField(
        max_digits=3, 
        decimal_places=0, 
        null=True, 
        blank=True, 
        choices=value_choices,
        verbose_name=u'1 - напряженный, 7 - Раскованный'
    )

    attractiveness = models.DecimalField(
        max_digits=3, 
        decimal_places=0, 
        null=True, 
        blank=True, 
        choices=value_choices,
        verbose_name=u'1 - Менее привлекательный, 7 - более привлекательный'
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


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


class Requirement(models.Model):
    value_choices = [
        (1, '1. Кандидат не владеет навыком'),
        (2, '2. Кандидат владеет навыком недостаточно'),
        (3, '3. Навык у кандидата проявляется достаточно четко'),
        (4, '4. Навык у кандидата проявляется со средней активностью'),
        (5, '5. Кандидат хорошо владеет навыком'),
        (6, '6. Кандидат владеет навыком очень хорошо'),
        (7, '7. Кандидат владеет навыком превосходно'),
    ]
    requirement_name = models.CharField(max_length=50, null=True, verbose_name=u'Название требуемого навыка')
    value = models.DecimalField(max_digits=5, decimal_places=0, null=True, choices=value_choices, verbose_name=u'Уровень владения требуемым навыком')
    position = models.ForeignKey(Position, on_delete=models.CASCADE)


class Skill(models.Model):
    value_choices = [
        (1, '1. Кандидат не владеет навыком'),
        (2, '2. Кандидат владеет навыком недостаточно'),
        (3, '3. Навык у кандидата проявляется достаточно четко'),
        (4, '4. Навык у кандидата проявляется со средней активностью'),
        (5, '5. Кандидат хорошо владеет навыком'),
        (6, '6. Кандидат владеет навыком очень хорошо'),
        (7, '7. Кандидат владеет навыком превосходно'),
    ]
    skill_name = models.CharField(max_length=50, null=True, verbose_name=u'Название навыка')
    value = models.DecimalField(max_digits=5, decimal_places=0, null=True, choices=value_choices, verbose_name=u'Уровень владения навыком')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)