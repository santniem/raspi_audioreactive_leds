 #!/usr/bin/env python3
from neopixel import *
import argparse
import socket


# LED strip configuration:
LED_COUNT      = 240    # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 25     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53



strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()


HOST = "192.168.0.9"   # The ip address of your raspberry pi
PORT = 5218            # Just a random open port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class mirrored:
    counter=0
    rcounter=0
    sizeCounter=0
    def __init__(self, offset,size,color):
        self.offset = offset
        self.size = size
        self.counter = offset
        self.rcounter= offset
        self.sizeCounter = 0
        self.color = color
    def move(self):  
        if(self.counter < self.offset+self.size):
            self.counter+=1
            for i in range(self.sizeCounter):
                strip.setPixelColor(self.counter-i-1, self.color)

        if(self.counter >= self.offset+self.size):
            self.counter+=1
            for k in range(self.size):
                strip.setPixelColor(self.counter-k, self.color)
				
        self.sizeCounter+=1
        if(self.sizeCounter >= self.size):
            self.sizeCounter = 0
        
        if(self.counter > 240):
            self.counter = self.offset
                
    def reversemove(self):
        if(self.rcounter > self.offset-self.size):
            self.rcounter-=1
            for i in range(self.sizeCounter):
                strip.setPixelColor(self.rcounter+i+2, self.color)
				
        if(self.rcounter <= self.offset-self.size):
            self.rcounter-=1
            for k in range(self.size):
                strip.setPixelColor(self.rcounter+k, self.color)  
				
        self.sizeCounter+=1
        if(self.sizeCounter >= self.size):
            self.sizeCounter = 0
        if(self.rcounter < 0):
            self.rcounter = self.offset

            
def blink(color):
"""this is here just because my desk is shaped like this
		/-----------\
	   /			 \
	  /				  \
"""
    for i in range(123,140):
        strip.setPixelColor(i, color)

def blink2():
    red= conn.recv(3)
    green= conn.recv(3)
    blue= conn.recv(3)
                
                
    red= filter(lambda x: x.isdigit(),red)
    green= filter(lambda x: x.isdigit(),green)
    blue= filter(lambda x: x.isdigit(),blue)
                
    if(red.isdigit() and green.isdigit() and blue.isdigit()):
        newcolor= red+green+blue
        colori = Color(int(green),int(red),int(blue))
        #print("RED: " + red + " Green: " + green  + " BLUE: " + blue)
        for i in range(LED_COUNT):
            strip.setPixelColor(i, colori)
        strip.show()
     


oldcolor = "000000000"

def scrollaus():
    red= conn.recv(3)
    green= conn.recv(3)
    blue= conn.recv(3)
                
                
    red= filter(lambda x: x.isdigit(),red)
    green= filter(lambda x: x.isdigit(),green)
    blue= filter(lambda x: x.isdigit(),blue)
                
    if(red.isdigit() and green.isdigit() and blue.isdigit()):
        newcolor= red+green+blue
        colori = Color(int(green),int(red),int(blue)) #GRB
        print("RED: " + red + " Green: " + green  + " BLUE: " + blue)
        obj = mirrored(140,1,colori)
        obj2 = mirrored(124,1,colori)
        objlist.append(obj)
        objlistr.append(obj2)
        for i in range(len(objlist)):
            objlist[i].move()
        for i in range(len(objlistr)):
            objlistr[i].reversemove()
             
        blink(colori)
                    
    oldcolor = red+green+blue
    strip.show()
        
    data=""
    if(len(objlist) >= LED_COUNT/2):
        objlist.pop(0)
    if(len(objlistr) >= LED_COUNT/2):
        objlistr.pop(0)
        
    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()
    s.bind((HOST, PORT))
    s.listen(5)
    conn, addr = s.accept()
    print('Connected by', addr)
    print ('Press Ctrl-C to quit.')

    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')
    
    try:
        objlist = []
        objlistr = []
        black = Color(0,0,0)
        while True:
            
            data = conn.recv(3)
            
            if(data=="sto"):
                print("connection closed")
                
                conn.close()
                blink(black)
                strip.show()
                conn, addr = s.accept()
                
            if(data== "led"):
                scrollaus()
                
            if (data =="bli"):
                blink2()

    except KeyboardInterrupt:
        if args.clear:
            blink(black)
            
                
