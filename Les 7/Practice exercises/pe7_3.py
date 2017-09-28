"""
    Title: Practice exercise 7_3
    Author: Floris de Kruijff
    Date created: 28-Sep-17
"""

results = {
    'student1': 4,
    'student2': 5,
    'student3': 9,
    'student4': 3,
    'student5': 4,
    'student6': 1,
    'student7': 10,
    'student8': 8,
}

for result in results:
    print("{} finished the course with a {}".format(result, results[result]))
