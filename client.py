import datetime
import socket
import time
import uuid
import pygame
import sys
from _thread import *

import RPi.GPIO as GPIO

HOST = '145.89.96.103'
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
    # Initialise display
    lcd_byte(0x33, LCD_CMD)  # 110011 Initialise
    lcd_byte(0x32, LCD_CMD)  # 110010 Initialise
    lcd_byte(0x06, LCD_CMD)  # 000110 Cursor move direction
    lcd_byte(0x0C, LCD_CMD)  # 001100 Display On,Cursor Off, Blink Off
    lcd_byte(0x28, LCD_CMD)  # 101000 Data length, number of lines, font size
    lcd_byte(0x01, LCD_CMD)  # 000001 Clear display
    time.sleep(LCD_E_DELAY)


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
    time.sleep(LCD_E_DELAY)
    GPIO.output(LCD_E, True)
    time.sleep(LCD_E_PULSE)
    GPIO.output(LCD_E, False)
    time.sleep(LCD_E_DELAY)


def lcd_string(message, line):
    message = message.ljust(LCD_WIDTH, " ")
    lcd_byte(line, LCD_CMD)
    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]), LCD_CHR)


def led_on(pin):
    GPIO.output(pin, GPIO.HIGH)


def led_off(pin):
    GPIO.output(pin, GPIO.LOW)


def button(x):
    y = GPIO.input(x)
    if not y:
        return True


def alarm_system_on():
    global system_on
    global LCD_text_1
    led_on(26)
    system_on = True
    socket_write("", "ALRM_ON")
    LCD_text_1 =' Sytem is on'
    time.sleep(0.2)


def alarm_system_off():
    global system_on
    global LCD_text_1
    led_off(26)
    led_off(19)
    led_off(13)
    system_on = False
    socket_write("", "ALRM_OFF")
    LCD_text_1 = ' Sytem is off'
    time.sleep(0.5)
    pygame.mixer.music.stop()


def flikker(x):
    while True:
        led_on(x)
        time.sleep(0.2)
        led_off(x)
        time.sleep(0.2)
        if system_on == False:

            led_off(x)
            break


def alarm_trigger():
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
        if time.time() - alarm_trigger_time >= trigger_delay and alarm_trigger_time != 0:
            pygame.mixer.music.play()
            socket_write("", "ALRM_TRIP")
            time.sleep(0.5)
            led_off(13)
            start_new_thread(flikker(19), ())
            print(alarm_tripped)
            break


def alarm_trigger_off():
    global server_disable_alarm
    global alarm_tripped
    led_off(19)
    server_disable_alarm = True
    alarm_tripped = False
    led_off(19)
    time.sleep(0.5)
    pygame.mixer.music.stop()


def gpio_mainloop():
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
    return datetime.datetime.now().strftime('%d-%m-%Y %X')


def has_timeout():
    while True:
        time.sleep(10)
        if time.time() - last_ping >= 5.5 and last_ping != 0:
            if debug: print("There is no longer a connection to the server, exiting system")
            global LCD_text_2
            LCD_text_2 = ' Not Connected'
            led_on(13)
            alarm_trigger()
            exit()


def parse_socket_data(data: str):
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
        return[0] = Client node UUID
        return[1] = data_header
        return[2] = data
    """
    global LCD_text_2
    message = str(UUID) + "," + data_header + "," + data
    if debug: print("{} - Client send: {}".format(get_time(), message))

    try:
        client_socket.send(message.encode('ascii'))
    except ConnectionResetError or ConnectionAbortedError:
        if debug: print("{} - Connection has been terminated by the server.".format(get_time()))
        LCD_text_2 = ' Not Connected'
        exit()
    client_socket.send(message.encode('ascii'))


def socket_read():
    data = None
    try:
        data = client_socket.recv(4096)
    except ConnectionResetError or ConnectionAbortedError or KeyboardInterrupt:
        if debug: print("{} - Connection has been terminated by the server.".format(get_time()))
        exit()
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
            exit()
        finally:
            if debug: print("{} - Successfully connect to IP:{}, PORT:{}".format(get_time(), HOST, PORT))

        lcd_init()
        start_new_thread(gpio_mainloop, ())
        start_new_thread(has_timeout, ())

        while True:
            socket_read()
    finally:
        lcd_byte(0x01, LCD_CMD)
        lcd_string(" Goodbye!", LCD_LINE_1)
        GPIO.output(26, 0)
        GPIO.output(19, 0)
        GPIO.output(13, 0)
