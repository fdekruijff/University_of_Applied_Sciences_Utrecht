"""
    Title: Practice exercise 6_4
    Author: Floris de Kruijff
    Date created: 21-Sep-17
"""

student_grades = [[95, 92, 86], [66, 75, 54], [89, 72, 100], [34, 0, 0]]


def average_per_student(grades):
    """ Returns the average of each student in a list with grades """
    average = ''
    for student_grade in grades:
        average = average + "Student has average of: {}{}".format(sum(student_grade) / len(student_grades), "\n")

    return average


def average_all_students(grades):
    """ Returns the average of all the student in a list with grades """
    value = 0

    for student_grade in grades:
        value += sum(student_grade) / len(student_grade)
    value /= len(grades)

    return value


print(average_per_student(student_grades))
print(average_all_students(student_grades))
