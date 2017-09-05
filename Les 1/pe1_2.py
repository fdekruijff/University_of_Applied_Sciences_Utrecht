"""
    Title: Practice exercise 1_2
    Author: Floris de Kruijff
    Date created: 04-Sep-17
"""

# A:
print(len('Supercalifragilisticexpialidocious'))

# B:
print('ice' in 'Supercalifragilisticexpialidocious')

# C:
print(len('ntidisestablishmentarianism') > len('Honorificabilitudinitatibus'))

# D:
componist = ['Berlioz', 'Borodin', 'Brian', 'Bartok', 'Bellini', 'Buxtehude', 'Bernstein']
componist.sort()
print(componist[0] + ' ' + componist[len(componist) - 1])