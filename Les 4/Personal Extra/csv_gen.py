"""
    Title: CSV file generator from input String
    Author: Floris de Kruijff
    Date created: 09-Sep-17
"""

input_string = """dinsdag 14-11-2017 (18:00 - 21:00 in zaal 2.05)
donderdag 16-11-2017 (18:00 - 21:00 in zaal 2.05)
dinsdag 21-11-2017 (18:00 - 21:00 in zaal 2.05)
donderdag 23-11-2017 (18:00 - 21:00 in zaal 2.05)
dinsdag 28-11-2017 (18:00 - 21:00 in zaal 2.05)
donderdag 30-11-2017 (18:00 - 21:00 in zaal 2.05)
dinsdag 05-12-2017 (18:00 - 21:00 in zaal 2.05)
donderdag 07-12-2017 (18:00 - 21:00 in zaal 2.05)
dinsdag 12-12-2017 (18:00 - 21:00 in zaal 2.05)
donderdag 14-12-2017 (18:00 - 21:00 in zaal 2.05)
maandag 08-01-2018 (18:00 - 21:00 in zaal 2.04)
woensdag 10-01-2018 (18:00 - 21:00 in zaal 2.04)
zaterdag 13-01-2018 (10:00 - 13:00 in zaal 2.04)
maandag 15-01-2018 (18:00 - 21:00 in zaal 2.04)
woensdag 17-01-2018 (18:00 - 21:00 in zaal 2.04)
zaterdag 20-01-2018 (10:00 - 13:00 in zaal 2.04)
maandag 22-01-2018 (18:00 - 21:00 in zaal 2.04)
woensdag 24-01-2018 (18:00 - 21:00 in zaal 2.04)
zaterdag 27-01-2018 (10:00 - 13:00 in zaal 2.04)
maandag 29-01-2018 (18:00 - 21:00 in zaal 2.04)
woensdag 31-01-2018 (18:00 - 21:00 in zaal 2.04)
zaterdag 03-02-2018 (10:00 - 13:00 in zaal 2.04)
maandag 05-02-2018 (18:00 - 21:00 in zaal 2.04)
woensdag 07-02-2018 (18:00 - 21:00 in zaal 2.04)
zaterdag 10-02-2018 (10:00 - 13:00 in zaal 2.04)
maandag 12-02-2018 (18:00 - 21:00 in zaal 2.04)
woensdag 14-02-2018 (18:00 - 21:00 in zaal 2.04)
zaterdag 17-02-2018 (10:00 - 13:00 in zaal 2.04)
maandag 19-02-2018 (18:00 - 21:00 in zaal 2.04)
woensdag 21-02-2018 (18:00 - 21:00 in zaal 2.04)
zaterdag 24-02-2018 (10:00 - 13:00 in zaal 2.04)
maandag 26-02-2018 (18:00 - 21:00 in zaal 2.04)
woensdag 28-02-2018 (18:00 - 21:00 in zaal 2.04)
zaterdag 03-03-2018 (10:00 - 13:00 in zaal 2.04)
maandag 05-03-2018 (18:00 - 21:00 in zaal 2.04)
woensdag 07-03-2018 (18:00 - 21:00 in zaal 2.04)
zaterdag 10-03-2018 (10:00 - 13:00 in zaal 2.04)
maandag 12-03-2018 (18:00 - 21:00 in zaal 2.04)
woensdag 14-03-2018 (18:00 - 21:00 in zaal 2.04)
zaterdag 17-03-2018 (10:00 - 13:00 in zaal 2.04)
maandag 19-03-2018 (18:00 - 21:00 in zaal 2.04)
woensdag 21-03-2018 (18:00 - 21:00 in zaal 2.04)
zaterdag 24-03-2018 (10:00 - 13:00 in zaal 2.04)
maandag 26-03-2018 (18:00 - 21:00 in zaal 2.04)
woensdag 28-03-2018 (18:00 - 21:00 in zaal 2.04)
woensdag 04-04-2018 (18:00 - 21:00 in zaal 2.04)
maandag 09-04-2018 (18:00 - 21:00 in zaal 2.04)
woensdag 11-04-2018 (18:00 - 21:00 in zaal 2.04)
zaterdag 14-04-2018 (10:00 - 13:00 in zaal 2.04)
maandag 16-04-2018 (18:00 - 21:00 in zaal 2.04)
"""

data_array = input_string.splitlines()

with open('output.csv', 'w') as output_file:
    # Setup headers
    output_file.write(
        str("Subject,Start Date,Start Time,End Date,End Time,All Day Event,Description,Location,Private")
    )
    output_file.write("\n")

    for appointment in data_array:
        appointment = appointment.split(' ')

        output_file.write("Boswell-Beta les," + str(appointment[1]).replace('-', '/') + "," + str(appointment[2])[1:] + "," + str(appointment[1]).replace('-', '/') + "," + str(appointment[4]) + ",false,Boswell-Beta VWO Wiskunde B Cursus," + str(appointment[6]) + " " + str(appointment[7])[:-1] + ",true")
        output_file.write("\n")

    output_file.close()