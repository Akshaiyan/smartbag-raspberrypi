 
import smbus
import time
from datetime import datetime
import time
daystructure = [["08 : 20" , "09 : 05"],["09 : 06" , "09 : 55"],["09 : 56" , "10 : 15"],["10 : 16" , "11 : 05"],["11 : 06" , "11 : 50"],["11 : 56" , "12 : 35"],["12 : 36" , "13 : 25"],["13 : 26" , "13 : 50"],["13 : 51" , "14 : 35"],["14 : 36" , "15 : 25"]]

    

# Convert datetime day number into day name
def day(daynum):
    if daynum ==  0:
        return "monday"
    elif daynum == 1:
        return "tuesday"
    elif daynum == 2:
        return "wednesday"
    elif daynum == 3:
        return "thursday"
    elif daynum == 4:
        return "friday"
    else:
        return "either something went wrong, or its a weekend!"
    
def gettimetable():
    
    dt = datetime.now()
    daynum = dt.weekday()
    txtday = day(daynum)
    text = r"/home/smartbag/timetable/"+txtday+".txt"
    timetable = []
    oFile = open(text, 'r')
    line = oFile.readlines()
    return line

def displaylesson(time):
    num = 0
    timespl = time.split(" : ")
    timespl = timespl[0] + timespl[1]
    for lesson in daystructure:
        num = num + 1
        startime = lesson[0].split(" : ")
        startime = startime[0] + startime[1]
        endtime = lesson[1].split(" : ")
        endtime = endtime[0] + endtime[1]
        #print(startime , endtime)
        if int(timespl) >=  (int(startime)) and int(timespl) <= (int(endtime)):
            spaces = (16 - len(gettimetable()[num - 1])) // 2
            finaldisplay = (" "*spaces+(gettimetable()[num] - 1))

            return finaldisplay
        
    return "   No Lessons!"
        
        
        
        
        


# Define some device parameters
I2C_ADDR  = 0x27 # I2C device address, if any error, change this address to 0x3f
LCD_WIDTH = 16   # Maximum characters per line

# Define some device constants
LCD_CHR = 1 # Mode - Sending data
LCD_CMD = 0 # Mode - Sending command

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line

LCD_BACKLIGHT  = 0x08  # On
#LCD_BACKLIGHT = 0x00  # Off

ENABLE = 0b00000100 # Enable bit

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

#Open I2C interface
#bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(1) # Rev 2 Pi uses 1

def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off 
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)

def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = the data
  # mode = 1 for data
  #        0 for command

  bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
  bits_low = mode | ((bits<<4) & 0xF0) | LCD_BACKLIGHT

  # High bits
  bus.write_byte(I2C_ADDR, bits_high)
  lcd_toggle_enable(bits_high)

  # Low bits
  bus.write_byte(I2C_ADDR, bits_low)
  lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
  # Toggle enable
  time.sleep(E_DELAY)
  bus.write_byte(I2C_ADDR, (bits | ENABLE))
  time.sleep(E_PULSE)
  bus.write_byte(I2C_ADDR,(bits & ~ENABLE))
  time.sleep(E_DELAY)

def lcd_string(message,line):
  # Send string to display

  message = message.ljust(LCD_WIDTH," ")

  lcd_byte(line, LCD_CMD)

  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)

def main():
    
  # Main program block

  # Initialise display
  lcd_init()



  while True:

    dt = datetime.now()
    timenow = dt.strftime("%H : %M")
    displaytime = dt.strftime("  %H : %M : %S")
      

    # Send some test
    lcd_string(displaylesson(timenow),LCD_LINE_1)
    lcd_string(displaytime,LCD_LINE_2)

    time.sleep(1)
  
if __name__ == '__main__':

  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    lcd_byte(0x01, LCD_CMD)
    
    
    
    
    
    


