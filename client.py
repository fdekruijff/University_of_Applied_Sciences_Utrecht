# import
import RPi.GPIO as GPIO
import time
#varible buttons
start = True
aan = False
alarm = False
text_1 = " Alarm is uit"
text_2 = " Niet verbonden "

# Define GPIO to LCD mapping
LCD_RS = 7
LCD_E = 8
LCD_D4 = 25
LCD_D5 = 24
LCD_D6 = 23
LCD_D7 = 18

# Define some device constants
LCD_WIDTH = 16  # Maximum characters per line
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80  # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0  # LCD RAM address for the 2nd line

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

def led_on(x):
    GPIO.output(x, GPIO.HIGH)


def led_off(x):
    GPIO.output(x, 0)

def button(x):
    y = GPIO.input(x)
    if y == False:
        return True

def aanzetten():
    if button(6) == True and aan == False:
        led_on(26)
        global aan
        aan = True
        global text_1
        text_1 = " Alarm is aan"
        time.sleep(0.2)

def uitzetten():
    if button(6) == True and aan == True:
        led_off(26)
        led_off(19)
        global aan
        global text_1
        aan = False
        text_1 = " Alarm is uit"
        time.sleep(0.5)

def alarmtrigger():
    if aan == True:
        if button(5) == True:
            led_on(19)

def alarmtrigger():
    if aan == True:
        if button(5) and button(6):
            led_on(19)
            led_off(19)
            led_on(5)

def main():
    # Main program block

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)  # Use BCM GPIO numbers
    GPIO.setup(LCD_E, GPIO.OUT)  # E
    GPIO.setup(LCD_RS, GPIO.OUT)  # RS
    GPIO.setup(LCD_D4, GPIO.OUT)  # DB4
    GPIO.setup(LCD_D5, GPIO.OUT)  # DB5
    GPIO.setup(LCD_D6, GPIO.OUT)  # DB6
    GPIO.setup(LCD_D7, GPIO.OUT)  # DB7
    GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Initialise display
    lcd_init()

    while True:

        if start == True:
            GPIO.setup(26, GPIO.OUT)
            GPIO.setup(19, GPIO.OUT)
            GPIO.setup(13, GPIO.OUT)
            global start
            start = False

        if button(6) == True and aan == False:
            led_on(26)
            global aan
            aan = True
            global text_1
            text_1= " Alarm is aan"
            time.sleep(0.2)

        if button(6) == True and aan == True:
            led_off(26)
            led_off(19)
            global aan
            global text_1
            aan = False
            text_1 = " Alarm is uit"
            time.sleep(0.5)

        if aan == True:
            if button(11) == True:
                led_on(19)
                global text_2
                text_2 = " joepie "

        if aan == True:
            if button(5) == True:
                led_on(19)
                global text_2
                text_2 = " joepie "
            print

        # Send some test
        lcd_string(text_1 + u' \u005C', LCD_LINE_1)
        lcd_string(text_2, LCD_LINE_2)
        #time.sleep(3)  # 3 second delay
        aanzetten()
        uitzetten()
        alarmtrigger()

        # Send some text
        #lcd_string(text_1 + ' |', LCD_LINE_1)
        lcd_string(text_2, LCD_LINE_2)

        # time.sleep(3)  # 3 second delay
        aanzetten()
        uitzetten()
        alarmtrigger()

        # Send some text
        #lcd_string(text_1+' /', LCD_LINE_1)
        lcd_string(text_2, LCD_LINE_2)
        #
        # time.sleep(3)
        aanzetten()
        uitzetten()
        alarmtrigger()

        # Send some text
        #lcd_string(text_1 + ' -', LCD_LINE_1)
        lcd_string(text_2, LCD_LINE_2)

        # time.sleep(3)


def lcd_init():
    # Initialise display
    lcd_byte(0x33, LCD_CMD)  # 110011 Initialise
    lcd_byte(0x32, LCD_CMD)  # 110010 Initialise
    lcd_byte(0x06, LCD_CMD)  # 000110 Cursor move direction
    lcd_byte(0x0C, LCD_CMD)  # 001100 Display On,Cursor Off, Blink Off
    lcd_byte(0x28, LCD_CMD)  # 101000 Data length, number of lines, font size
    lcd_byte(0x01, LCD_CMD)  # 000001 Clear display
    time.sleep(E_DELAY)


def lcd_byte(bits, mode):
    # Send byte to data pins
    # bits = data
    # mode = True  for character
    #        False for command

    GPIO.output(LCD_RS, mode)  # RS

    # High bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits & 0x10 == 0x10:
        GPIO.output(LCD_D4, True)
    if bits & 0x20 == 0x20:
        GPIO.output(LCD_D5, True)
    if bits & 0x40 == 0x40:
        GPIO.output(LCD_D6, True)
    if bits & 0x80 == 0x80:
        GPIO.output(LCD_D7, True)

    # Toggle 'Enable' pin
    lcd_toggle_enable()

    # Low bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits & 0x01 == 0x01:
        GPIO.output(LCD_D4, True)
    if bits & 0x02 == 0x02:
        GPIO.output(LCD_D5, True)
    if bits & 0x04 == 0x04:
        GPIO.output(LCD_D6, True)
    if bits & 0x08 == 0x08:
        GPIO.output(LCD_D7, True)

    # Toggle 'Enable' pin
    lcd_toggle_enable()


def lcd_toggle_enable():
    # Toggle enable
    time.sleep(E_DELAY)
    GPIO.output(LCD_E, True)
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, False)
    time.sleep(E_DELAY)


def lcd_string(message, line):
    # Send string to display




    message = message.ljust(LCD_WIDTH, " ")

    lcd_byte(line, LCD_CMD)

    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]), LCD_CHR)


if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        lcd_byte(0x01, LCD_CMD)
        lcd_string(" Goodbye!", LCD_LINE_1)
        GPIO.output(26, 0)
        GPIO.output(19, 0)
        GPIO.output(13, 0)
        GPIO.cleanup()

=======
import socket
import time
import uuid
from _thread import *

HOST = '192.168.42.2'
PORT = 5555
UUID = uuid.uuid4().hex

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

connected = False
registered = False
alarm_tripped = False
alarm_enabled = False
alarm_interval_seconds = 5


def parse_socket_data(data: str):
    if data == "REG_COMPLETE":
        registered = True
    elif data == "ALRM_TRIP":
        pass
    elif data == "ALRM_STOP":
        pass
    elif data == "ALRM_ON":
        pass
    elif data == "ALRM_OFF":
        pass
    elif data == "CHNG_INTERVAL":
        pass
    elif data == "IS_ALIVE":
        socket_write("ACK", "")
    elif data == "UUID_REQ":
        socket_write(str(UUID), "UUID")


def socket_write(data: str, data_header: str):
    """
        return[0] = Client node UUID
        return[1] = data_header
        return[2] = data
    """
    message = str(UUID) + "," + data_header + "," + data
    client_socket.send(message.encode('ascii'))


def socket_is_alive():
    while True:
        socket_write("IS_ALIVE", "")
        data = client_socket.recv(2048).decode('utf-8').strip()
        print(data)
        if data == "ACK":
            connected = True
        else:
            connected = False
        time.sleep(1)


def socket_read():
    data = client_socket.recv(2048)
    data = data.decode('utf-8').strip().split(',')
    if (data[0] == UUID) or (data[0] == "BROADCAST"):
        return parse_socket_data(data[1])

    if not connected:
        print("Not connected anymore")


if __name__ == '__main__':
    try:
        client_socket.connect((HOST, PORT))
        connected = True
    except socket.error as e:
        print("Socket error {}".format(e))
        exit()
    finally:
        print("Successfully connect to IP:{}, PORT:{}".format(HOST, PORT))

    start_new_thread(socket_is_alive, ())
    while True:
        socket_read()