"""
    Computer Systems and Networks
    University of Applied Sciences Utrecht
    TICT-V1CSN-15 Project
"""

import datetime
import socket
import time
import sys
import uuid
import pygame

import RPi.GPIO as GPIO

from _thread import *


HOST = ''  # Enter IP address of device where server.py is running
PORT = 5555
UUID = uuid.uuid4().hex
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# var GPIO
run = True
connected_to_server = False
registered = False
debug = True
last_ping = 0
alarm_tripped = False
alarm_enabled = False
alarm_interval_seconds = 5
alarm_running = True
system_on = False
alarm_trigger_time = 0
alarm_on = False
trigger_delay = 5
server_disable_alarm = False

pygame.mixer.init()
pygame.mixer.music.load("shootingstars.mp3")


# LCD var declarations
LCD_RS = 7
LCD_E = 8
LCD_D4 = 25
LCD_D5 = 24
LCD_D6 = 23
LCD_D7 = 18
LCD_WIDTH = 16
LCD_CHR = True
LCD_CMD = False
LCD_LINE_1 = 0x80
LCD_LINE_2 = 0xC0
LCD_E_PULSE = 0.0005
LCD_E_DELAY = 0.0005
LCD_text_1 = " Alarm is off "
LCD_text_2 = " Not connected_to_server "

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
GPIO.setup(26, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)


def lcd_init():
    """ Initialise display """
    lcd_byte(0x33, LCD_CMD)  # 110011 Initialise
    lcd_byte(0x32, LCD_CMD)  # 110010 Initialise
    lcd_byte(0x06, LCD_CMD)  # 000110 Cursor move direction
    lcd_byte(0x0C, LCD_CMD)  # 001100 Display On,Cursor Off, Blink Off
    lcd_byte(0x28, LCD_CMD)  # 101000 Data length, number of lines, font size
    lcd_byte(0x01, LCD_CMD)  # 000001 Clear display
    time.sleep(LCD_E_DELAY)


def lcd_byte(bits, mode):
    """ Send byte to data pins """
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
    """ Toggle enable """
    time.sleep(LCD_E_DELAY)
    GPIO.output(LCD_E, True)
    time.sleep(LCD_E_PULSE)
    GPIO.output(LCD_E, False)
    time.sleep(LCD_E_DELAY)


def lcd_string(message, line):
    """ Writes message to LCD on specified line """
    message = message.ljust(LCD_WIDTH, " ")
    lcd_byte(line, LCD_CMD)
    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]), LCD_CHR)


def led_on(pin):
    """ Turns pin to 1 """
    GPIO.output(pin, GPIO.HIGH)


def led_off(pin):
    """ Turns pin to 0 """
    GPIO.output(pin, GPIO.LOW)


def button(x):
    """ returns whether button is pressed or not """
    y = GPIO.input(x)
    if not y:
        return True


def alarm_system_on():
    """ Turn alarm system on, update hardware, software and server accordingly """
    global system_on
    global LCD_text_1
    led_on(26)
    system_on = True
    socket_write("", "ALRM_ON")
    LCD_text_1 = ' System is on'
    time.sleep(0.2)


def alarm_system_off():
    """ Turn alarm system off, update hardware, software and server accordingly """
    global system_on
    global LCD_text_1
    led_off(26)
    led_off(19)
    led_off(13)
    system_on = False
    socket_write("", "ALRM_OFF")
    LCD_text_1 = ' System is off'
    time.sleep(0.5)
    pygame.mixer.music.stop()


def led_flicker(x):
    """ Turns pin x on and off until told otherwise """
    while True:
        led_on(x)
        time.sleep(0.2)
        led_off(x)
        time.sleep(0.2)
        if not system_on:
            led_off(x)
            break


def alarm_trigger():
    """ Triggers alarm, waits trigger_delay time before updating hardware, software and server """
    global server_disable_alarm
    alarm_tripped = True
    led_on(13)
    while system_on:
        if button(6):
            break
        if server_disable_alarm:
            server_disable_alarm = False
            break
        global alarm_tripped
        if (time.time() - alarm_trigger_time >= trigger_delay) and (alarm_trigger_time != 0):
            pygame.mixer.music.play()
            socket_write("", "ALRM_TRIP")
            time.sleep(0.5)
            led_off(13)
            start_new_thread(led_flicker(19), ())
            break


def alarm_trigger_off():
    """ Turns the alarm off """
    global server_disable_alarm
    global alarm_tripped
    led_off(19)
    server_disable_alarm = True
    alarm_tripped = False
    led_off(19)
    time.sleep(0.5)
    pygame.mixer.music.stop()


def gpio_mainloop():
    """ Contains general GPIO logic for LED, LCD and buttons """
    global alarm_running
    global system_on
    global alarm_trigger_time
    global LCD_text_1
    global LCD_text_2
    GPIO.output(26, 0)
    GPIO.output(19, 0)
    GPIO.output(13, 0)

    while True:
        if button(6) and system_on == False:
            alarm_system_on()

        if button(6) and system_on:
            alarm_system_off()

        if button(11) and system_on == True:
            alarm_trigger_time = time.time()
            start_new_thread (alarm_trigger, ())
            print (system_on)

        if button(5) and system_on == True:
            alarm_trigger_time = time.time()
            alarm_trigger()
        lcd_string(LCD_text_1, LCD_LINE_1)
        lcd_string(LCD_text_2, LCD_LINE_2)


def get_time():
    """ Returns current time in format %d-%m-%Y %X """
    return datetime.datetime.now().strftime('%d-%m-%Y %X')


def has_timeout():
    """ Check if the client is no longer connected if it has not received socket data for more than 5.5 seconds """
    while True:
        time.sleep(10)
        if time.time() - last_ping >= 5.5 and last_ping != 0:
            if debug: print("There is no longer a connection to the server, exiting system")
            global LCD_text_2
            LCD_text_2 = ' Not Connected'
            led_on(13)
            alarm_trigger()
            stop_client()
            sys.exit()


def parse_socket_data(data: str):
    """ Handles socket data accordingly """
    global registered
    global last_ping
    global server_disable_alarm
    if data == "REG_COMPLETE":
        registered = True
    elif data == "ALRM_CHNG":
        if alarm_tripped:
            alarm_trigger_off()
        else:
            alarm_trigger()
    elif data == "ALRM_STATUS":
        pass
    elif data == "ALRM_TRIP":
        alarm_trigger()
    elif data == "ALRM_STOP":
        alarm_trigger_off()
    elif data == "ALRM_ON":
        alarm_system_on()
    elif data == "ALRM_OFF":
        server_disable_alarm = True
        alarm_system_off()
    elif data == "CHNG_INTERVAL":
        pass
    elif data == "IS_ALIVE":
        socket_write("ACK", "IS_ALIVE")
        last_ping = time.time()
        global LCD_text_2
        LCD_text_2= ' Connected'
    elif data == "UUID_REQ":
        socket_write(str(UUID), "UUID")
    elif data == "STATUS_UPD":
        socket_write("{'online': " + str(alarm_tripped) + "}", "STATUS_UPDM")


def socket_write(data: str, data_header: str):
    """
        Writes a concatenation of the client UUID, data header and data to
        the connection socket of this program instance
    """
    global LCD_text_2
    message = str(UUID) + "," + data_header + "," + data
    if debug: print("{} - Client send: {}".format(get_time(), message))

    try:
        client_socket.send(message.encode('ascii'))
    except ConnectionResetError or ConnectionAbortedError:
        if debug: print("{} - Connection has been terminated by the server.".format(get_time()))
        LCD_text_2 = ' Not Connected'
        stop_client()
        sys.exit()
    client_socket.send(message.encode('ascii'))


def stop_client():
    """ Cleans up GPIO when exiting """
    lcd_byte(0x01, LCD_CMD)
    lcd_string(" Goodbye!", LCD_LINE_1)
    GPIO.output(26, 0)
    GPIO.output(19, 0)
    GPIO.output(13, 0)
    

def socket_read():
    """
        Listens to the connection socket of this program instance
        and passes that data to the parse_socket_data() function
    """
    try:
        data = client_socket.recv(4096)
    except ConnectionResetError or ConnectionAbortedError or KeyboardInterrupt:
        if debug: print("{} - Connection has been terminated by the server.".format(get_time()))
        stop_client()
        sys.exit()
    data = data.decode('utf-8').strip().split(',')
    if data[0] == '':

        alarm_trigger()
    if debug: print("{} - Client received: {}".format(get_time(), data))
    if (data[0] == UUID) or (data[0] == "BROADCAST"):
        return parse_socket_data(data[1])


if __name__ == '__main__':
    try:
        try:
            client_socket.connect((HOST, PORT))
            connected_to_server = True
        except socket.error as e:
            if debug: print("{} - Socket error {}".format(get_time(), e))
            sys.exit()
        finally:
            if debug: print("{} - Successfully connect to IP:{}, PORT:{}".format(get_time(), HOST, PORT))

        lcd_init()
        start_new_thread(gpio_mainloop, ())
        start_new_thread(has_timeout, ())

        while True:
            socket_read()
    finally:
        stop_client()
