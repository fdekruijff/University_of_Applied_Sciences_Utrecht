# importeer de GPIO bibliotheek.
import RPi.GPIO as GPIO
# Importeer de time biblotheek voor tijdfuncties.
from time import sleep
import time

# Zet de pinmode op Broadcom SOC.
GPIO.setmode(GPIO.BCM)
# Zet waarschuwingen uit.
GPIO.setwarnings(False)
#afstand 4096 is 1 rondje op de stapmotor
afstand = 5096
status = 'open'

#GPIO comminucatie
GPIO.setup(20,GPIO.OUT)
GPIO.setup (21, GPIO.IN)
GPIO.setup(16, GPIO.IN)

# set GPIO Pins
GPIO_TRIGGER = 2
GPIO_ECHO = 3
# set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

print ('GPIO setup done')

#meet afstand van sonic sensor
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return distance

#sluit de kering
def sluitkering_motor():
    # Stel de GPIO pinnen in voor de stappenmotor:
    StepPins = [5, 6, 13, 26]

    # Set alle pinnen als uitgang.
    for pin in StepPins:
        print("Setup pins")
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, False)

    # Definieer variabelen.
    StepCounter = 0

    # Definieer simpele volgorde
    StepCount1 = 4
    Seq1 = []
    Seq1 = range(0, StepCount1)
    Seq1[0] = [1, 0, 0, 0]
    Seq1[1] = [0, 1, 0, 0]
    Seq1[2] = [0, 0, 1, 0]
    Seq1[3] = [0, 0, 0, 1]

    # Definieer geadvanceerde volgorde (volgens de datasheet)
    StepCount2 = 8
    Seq2 = []
    Seq2 = range(0, StepCount2)
    Seq2[0] = [1, 0, 0, 0]
    Seq2[1] = [1, 1, 0, 0]
    Seq2[2] = [0, 1, 0, 0]
    Seq2[3] = [0, 1, 1, 0]
    Seq2[4] = [0, 0, 1, 0]
    Seq2[5] = [0, 0, 1, 1]
    Seq2[6] = [0, 0, 0, 1]
    Seq2[7] = [1, 0, 0, 1]

    # Welke stappenvolgorde gaan we hanteren?
    Seq = Seq2
    StepCount = StepCount2
    # afstand
    # 4096 is 1 rondje op de stapmotor
    status = 'open'
    StepCounter = 0
    for rond in range(0, afstand):
        for pin in range(0, 4):
            xpin = StepPins[pin]
            if Seq[StepCounter][pin] != 0:
                print "Stap: %i GPIO Actief: %i" % (StepCounter, xpin)
                GPIO.output(xpin, True)
            else:
                GPIO.output(xpin, False)

        StepCounter += 1

        # Als we aan het einde van de stappenvolgorde zijn beland start dan opnieuw
        if (StepCounter == StepCount): StepCounter = 0
        if (StepCounter < 0): StepCounter = StepCount

        # Wacht voor de volgende stap (lager = snellere draaisnelheid)
        sleep(.001)

    print ('kering is gesloten')

#opent de kering
def openkering_motor():
    # Stel de GPIO pinnen in voor de stappenmotor:
    StepPins = [26, 13, 6, 5]

    # Set alle pinnen als uitgang.
    for pin in StepPins:
        print "Setup pins"
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, False)

    # Definieer variabelen.
    StepCounter = 0

    # Definieer simpele volgorde
    StepCount1 = 4
    Seq1 = []
    Seq1 = range(0, StepCount1)
    Seq1[0] = [1, 0, 0, 0]
    Seq1[1] = [0, 1, 0, 0]
    Seq1[2] = [0, 0, 1, 0]
    Seq1[3] = [0, 0, 0, 1]

    # Definieer geadvanceerde volgorde (volgens de datasheet)
    StepCount2 = 8
    Seq2 = []
    Seq2 = range(0, StepCount2)
    Seq2[0] = [1, 0, 0, 0]
    Seq2[1] = [1, 1, 0, 0]
    Seq2[2] = [0, 1, 0, 0]
    Seq2[3] = [0, 1, 1, 0]
    Seq2[4] = [0, 0, 1, 0]
    Seq2[5] = [0, 0, 1, 1]
    Seq2[6] = [0, 0, 0, 1]
    Seq2[7] = [1, 0, 0, 1]

    # Welke stappenvolgorde gaan we hanteren?
    Seq = Seq2
    StepCount = StepCount2

    # Set alle pinnen als uitgang.
    StepCounter = 0
    for rond in range(0, afstand):
        for pin in range(0, 4):
            xpin = StepPins[pin]
            if Seq[StepCounter][pin] != 0:
                print "Stap: %i GPIO Actief: %i" % (StepCounter, xpin)
                GPIO.output(xpin, True)
            else:
                GPIO.output(xpin, False)

        StepCounter += 1

        # Als we aan het einde van de stappenvolgorde zijn beland start dan opnieuw
        if (StepCounter == StepCount): StepCounter = 0
        if (StepCounter < 0): StepCounter = StepCount

        # Wacht voor de volgende stap (lager = snellere draaisnelheid)
        sleep(0.001)
    print ('kering is geopend ')

def Main_loop_kering():
    #main loop
    try:
        while True:
            dist = distance()
            if dist <= 10 and status == 'open':
                print ("Sluit waterkering")
                sluitkering_motor()
                status = "dicht"
            elif dist > 10 and status == 'dicht':
                print ("Open waterkering")
                openkering_motor()
                status = "open"
            else:
                print ("Gemeten door_distance = %.1f cm" % dist)
            time.sleep(1)


    except KeyboardInterrupt:
        # GPIO netjes afsluiten
        GPIO.cleanup()

Main_loop_kering()
