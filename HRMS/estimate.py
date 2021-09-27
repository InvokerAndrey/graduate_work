import math


def get_skills_grades(employees):
    skills_grades = list()
    for employee in employees:
        for skill in employee.skill_set.all():
            skills_values = []
            skills_values.append(skill.value)
        skill_grade = round(sum(skills_values) / len(skills_values))
        skills_grades.append(skill_grade)

    return skills_grades


def get_requirement_grade(position):
    requirement_values = []
    for requirement in position.requirement_set.all():
        requirement_values.append(requirement.value)
    
    requirement_grade = round(sum(requirement_values) / len(requirement_values))

    return requirement_grade


def get_skills_raitings(employees, position):
    skills_required = dict()
    for skill_required in position.requirement_set.all():
        skills_required[skill_required.requirement_name] = skill_required.value

    g = 0.37
    value_seekers = list()
    for employee in employees:
        skills = {}
        d_list = []

        for skill in employee.skill_set.all():
            skills[skill.skill_name] = skill.value
        for skill_required, value_required in skills_required.items():
            try:
                d = int(value_required) - int(skills[skill_required])
            except KeyError:
                d = int(value_required)
                print(f'НЕ ХВАТАЕТ НАВЫКА {skill_required}: {value_required} ДЛЯ {position.position_name} У {employee.first_name} {employee.last_name}')
            
            d_list.append(d)

        d = round(sum(d_list) / len(d_list))
        value_seeker = (d * g) ** 2
        value_seekers.append(value_seeker)

    return value_seekers



def get_education_raitings(employees, position):
    education_required = int(position.education)

    g = 0.26
    value_seekers = list()

    for employee in employees:
        d = education_required - int(employee.education)
        value_seeker = (d * g) ** 2
        value_seekers.append(value_seeker)

    return value_seekers


def get_experience_raitings(employees, position):
    experience_required = int(position.experience)

    g = 0.15
    value_seekers = list()

    for employee in employees:
        d = experience_required - int(employee.experience)
        value_seeker = (d * g) ** 2
        value_seekers.append(value_seeker)

    return value_seekers


def get_personality_raitings(employees, position):
    sociability_required = int(position.sociability)
    smart_required = int(position.smart)
    emotionality_required = int(position.emotionality)
    self_centeredness_required = int(position.self_centeredness)
    tension_required = int(position.tension)

    g = 0.14
    value_seekers = list()
    for employee in employees:
        d1 = sociability_required - int(employee.sociability)
        d2 = smart_required - int(employee.smart)
        d3 = emotionality_required - int(employee.emotionality)
        d4 = self_centeredness_required - int(employee.self_centeredness)
        d5 = tension_required - int(employee.tension)

        d = round((d1 + d2 + d3 + d4 + d5) / 5)

        value_seeker = (d * g) ** 2
        value_seekers.append(value_seeker)

    return value_seekers


def get_appearance_raitings(employees, position):
    attractiveness_required = int(position.attractiveness)

    g = 0.08
    value_seekers = list()

    for employee in employees:
        d = attractiveness_required - int(employee.attractiveness)
        value_seeker = (d * g) ** 2
        value_seekers.append(value_seeker)

    return value_seekers


def get_estimated_employees(employees, position):
    skills_raitings = get_skills_raitings(employees, position)
    education_raitings = get_education_raitings(employees, position)
    experience_raitings = get_experience_raitings(employees, position)
    personality_raitings = get_personality_raitings(employees, position)
    appearance_raitings = get_appearance_raitings(employees, position)

    estimated_employees = dict()
    c_list = list()
    employees_list = list()
    best_employees = list()
    for employee, index in zip(employees, range(len(education_raitings))):
        employees_list.append(employee)

        summ = skills_raitings[index] + education_raitings[index] + experience_raitings[index]
        summ += personality_raitings[index] + appearance_raitings[index]

        c = math.sqrt(summ)
        c_list.append(c)
        estimated_employees[employee] = c

    min_c = min(c_list)
    index = 0
    min_index = 0
    min_indexes = list()
    for c in c_list:
        if c == min_c:
            min_index = index
            min_indexes.append(min_index)
        index += 1
    
    for min_index in min_indexes:
        best_employees.append(employees_list[min_index])

    return [estimated_employees, best_employees]