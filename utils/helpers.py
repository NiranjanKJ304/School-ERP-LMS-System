from config.settings import GROUP_SUBJECTS, SUBJECTS_1_10

def get_subjects_for_class(class_num, group=None):
    if class_num in [11, 12]:
        if group and group in GROUP_SUBJECTS:
            return GROUP_SUBJECTS[group]
        return []
    else:
        return SUBJECTS_1_10

def calculate_grade(percentage):
    if percentage >= 90:
        return 'A+'
    elif percentage >= 80:
        return 'A'
    elif percentage >= 70:
        return 'B+'
    elif percentage >= 60:
        return 'B'
    elif percentage >= 50:
        return 'C'
    elif percentage >= 40:
        return 'D'
    else:
        return 'F'

def calculate_result(percentage):
    return 'Pass' if percentage >= 40 else 'Fail'