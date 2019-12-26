def education_raitings(employees, position):
    matrix = [
        [3, 4, 5, 6, 7, 7, 7],
        [2, 3, 4, 5, 6, 7, 7],
        [1, 2, 3, 4, 5, 6, 7],
        [1, 1, 1, 3, 5, 6, 7],
        [1, 1, 1, 2, 5, 6, 7],
        [1, 1, 1, 1, 2, 5, 7],
        [1, 1, 1, 1, 2, 4, 7],
    ]
    print(matrix)
    educations = list()
    raitings = list()
    for employee in employees:
        for education in employee.education_set.all():
            if education.education_type:
                educations.append(education.education_type)
        if educations:
            i = int(position.education_required)
            j = int(max(educations))
            raiting = matrix[i][j]
            raitings.append(raiting)
        else:
            i = int(position.education_required)
            j = 0
            raiting = matrix[i][j]
            raitings.append(raiting)
        
        print(f'Образование: {employee.last_name}: i = {i}, j = {j}, raiting = {raiting}')
    print(f'raitings: {raitings}')

    return raitings


def experience_raitings(employees, position):
    matrix = [
        [3, 4, 5, 6, 7, 7],
        [2, 3, 4, 5, 6, 7],
        [1, 2, 3, 5, 6, 7],
        [1, 1, 2, 3, 5, 7],
        [1, 1, 1, 2, 3, 5],
        [1, 1, 1, 1, 2, 7]
    ]
    raitings = list()
    for employee in employees:
        experiences = 0
        for experience in employee.experience_set.all():
            if experience.job:
                exp = experience.expiration_date - experience.beginning_date
                exp_years = exp.days / 365
                experiences += exp_years
            experiences = int(experiences)

        i = int(position.experience_required)
        if experiences > 5:
            j = 5
        else:
            j = int(experiences)

        raiting = matrix[i][j]
        print(f'Опыт работы: {employee.last_name}: i = {i}, j = {j}, raiting = {raiting}')
        raitings.append(raiting)
    print(raitings)
    return raitings
        
                
def language_raitings(employees, position):
    matrix = [
        [3, 4, 5, 6, 7, 7, 7],
        [2, 3, 4, 5, 6, 7, 7],
        [1, 2, 3, 4, 5, 6, 7],
        [1, 1, 2, 3, 5, 6, 7],
        [1, 1, 1, 2, 3, 5, 7],
        [1, 1, 1, 1, 2, 4, 7],
        [1, 1, 1, 1, 2, 2, 7],
    ]
    raitings = list()
    for employee in employees:
        lang = False
        for language in employee.foreignlanguage_set.all():
            if position.foreign_language == 'Нет':
                lang = language
            if language.language_name == position.foreign_language:
                lang = language
        if lang:
            if position.language_level == None:
                i = 0
            else:
                i = int(position.language_level)

            if lang.level == None:
                j = 0
            else:
                j = int(lang.level)

            raiting = matrix[i][j]
        else:
            j = 0
            if position.language_level:
                i = int(position.language_level)
            else:
                i = 0
            raiting = matrix[i][j]

        raitings.append(raiting)
        print(f'Язык: {employee.last_name}: i = {i}, j = {j}, raiting = {raiting}')
    print(raitings)
    return raitings


def personality_raitings(employees, position):
    deviation = {
        0: 7,
        1: 6,
        2: 5,
        3: 4,
        4: 3,
        5: 2,
        6: 1,
    }
    difference = 0
    results = list()
    for employee in employees:
        raitings = []
        if employee.sociability:
            if position.sociability:
                defference = abs(int(position.sociability) - int(employee.sociability))
                raitings.append(deviation[defference])
            else:
                raitings.append(3)
        else:
            if position.sociability:
                raitings.append(1)
            else:
                raitings.append(3)

        if employee.smart:
            if position.smart:
                defference = abs(int(position.smart) - int(employee.smart))
                raitings.append(deviation[defference])
            else:
                raitings.append(3)
        else:
            if position.smart:
                raitings.append(1)
            else:
                raitings.append(3)

        if employee.emotionality:
            if position.emotionality:
                defference = abs(int(position.emotionality) - int(employee.emotionality))
                raitings.append(deviation[defference])
            else:
                raitings.append(3)
        else:
            if position.emotionality:
                raitings.append(1)
            else:
                raitings.append(3)

        if employee.self_centeredness:
            if position.self_centeredness:
                defference = abs(int(position.self_centeredness) - int(employee.self_centeredness))
                raitings.append(deviation[defference])
            else:
                raitings.append(3)
        else:
            if position.self_centeredness:
                raitings.append(1)
            else:
                raitings.append(3)
        
        if employee.tension:
            if position.tension:
                defference = abs(int(position.tension) - int(employee.tension))
                raitings.append(deviation[defference])
            else:
                raitings.append(3)
        else:
            if position.tension:
                raitings.append(1)
            else:
                raitings.append(3)

        average = round(sum(raitings) / 5)
        print(f'Личность: {employee.last_name}: average = {average}')
        results.append(average)
    print(f'Личность: results = {results}')
    return results


def appearance_raitings(employees, position):
    positive_deviation = {
        0: 3,
        1: 4,
        2: 5,
        3: 6,
        4: 7,
        5: 7,
        6: 7,
    }
    negative_deviation = {
        1: 2,
        2: 2,
        3: 1,
        4: 1,
        5: 1,
        6: 1,
    }
    raitings = list()
    for employee in employees:
        if employee.attractiveness:
            if position.attractiveness:
                defference = int(position.attractiveness) - int(employee.attractiveness)
                if defference <= 0:
                    raitings.append(positive_deviation[abs(defference)])
                else:
                    raitings.append(negative_deviation[abs(defference)])
            else:
                raitings.append(3)
        else:
            if position.attractiveness:
                raitings.append(1)
            else:
                raitings.append(3)

    print(f'Внешний облик: results = {raitings}')
    return raitings


def position_profile(position):
    if position.foreign_language:
        language = int(position.language_level)
    else:
        language = 1

    education = int(position.education_required)
    experience = int(position.experience_required)
    personality = round(
        int(position.sociability + position.smart + position.emotionality + position.self_centeredness + position.tension) / 5
    )
    appearance = int(position.attractiveness)
    result = round((language * 0.37) + (education * 0.26) + (experience * 0.15) + (personality * 0.14) + (appearance * 0.08))
    return [language, education, experience, personality, appearance, result]