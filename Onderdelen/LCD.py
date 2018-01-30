
# import
import RPi.GPIO as GPIO
import time



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

def lcd_kering_status():
    #vraag status op

    #status
    keringstatus = True
    if keringstatus == True:
        return "kering is dicht"
    else:
        return "kering is open"

def status_rasbberry(x):
    if x == 1:
        input_value = GPIO.input(16)
        if input_value == True:
            return 'PI 1  actief'
        elif input_value == False:
            return 'PI 1 Inactief'
    elif x == 2:
        input_value = GPIO.input(12)
        if input_value == True:
            return 'PI 2  actief'
        elif input_value == False:
            return 'PI 2 Inactief'

def switch_status():
    input_value21 = GPIO.input(21)
    input_value20 = GPIO.input(20)

    if input_value21 == True:
        return 0
    elif input_value20 == True:
        return 1
    else:
        return 2


def waterhoogte():
    hoogte = '10'
    return hoogte

def has_timeout():
    """ Check if the client is no longer connected if it has not received socket data for more than 5.5 seconds """
    while True:
        time.sleep(10)
        if time.time() - last_ping >= 5.5 and last_ping != 0:
            if debug: print("There is no longer a connection to the server, exiting system")
            global LCD_text_2
            LCD_text_2 = ' Not Connected'

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
    GPIO.setup(21, GPIO.IN)       # schakelaar
    GPIO.setup(20, GPIO.IN)       # schakelaar
    GPIO.setup(16, GPIO.IN)       #raspberry 1
    GPIO.setup(12, GPIO.IN)       #raspberry 2

    # Initialise display
    lcd_init()


    while True:
        #status raspberry
        if switch_status() == 0:
            time.sleep(0.5)
            if switch_status() == 0:
                while True:
                    lcd_string(status_rasbberry(1), LCD_LINE_1)
                    lcd_string(status_rasbberry(0), LCD_LINE_2)
                    if switch_status() != 0:
                        time.sleep(0.5)
                        if switch_status() != 0:
                            break

        #status pijl
        elif switch_status() == 1:
            time.sleep(0.5)
            if switch_status() == 1:
                while True:
                    lcd_string("Water niveau", LCD_LINE_1)
                    lcd_string(waterhoogte(), LCD_LINE_2)
                    if switch_status() != 1:
                        time.sleep(0.5)
                        if switch_status() != 1:
                            break
        elif switch_status() == 2:
            time.sleep(0.5)
            if switch_status() == 2:
                lcd_string(kering_status(), LCD_LINE_1)
                lcd_string("", LCD_LINE_2)
                if switch_status() != 2:
                    time.sleep(0.5)
                    if switch_status() != 2:
                        break


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
        lcd_string("Goodbye!", LCD_LINE_1)
        GPIO.cleanup()
