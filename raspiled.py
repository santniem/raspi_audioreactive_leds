 #!/usr/bin/env python3
from neopixel import *
import argparse
import socket
import time
import errno
from socket import error as socket_error
# LED strip configuration:
LED_COUNT      = 48    # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53



strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()


HOST = "192.168.0.7"   # The ip address of your raspberry pi
PORT = 5221      # Just a random open port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
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
        
        if(self.counter > LED_COUNT):
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
            
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()
    time.sleep(wait_ms/1000.0)
            
def blink(color):

    for i in range(27,27):
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
     
def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=15, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    dead = False
    for j in range(256*iterations):
        try:
            data=conn.recv(9)
        except socket_error,e:
            print ("Error sending data: %s" % e)

        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

    if(data == ""):
        return True
    if(data != ""):
        return False

def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)


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
		obj = mirrored(25,1,colori)
		obj2 = mirrored(27,1,colori)
		objlist.append(obj)
		objlistr.append(obj2)
		for i in range(len(objlist)):
			objlist[i].move()
		for i in range(len(objlistr)):
			objlistr[i].reversemove()
             
		blink(colori)
                    

	strip.show()
        
	data=""
	if(len(objlist) >= LED_COUNT/2):
		objlist.pop(0)
	if(len(objlistr) >= LED_COUNT/2):
		objlistr.pop(0)
	if(red == ''):
		print(red,green,blue)
		return True
	else:
		return False
def socketisded():
	while True:
		rainbow(strip)
		#print("sdg")
		##s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#try:
			#conn, addr = s.accept()
		#except:
			#pass
		#conn.send("ready")
		#ass=conn.recv(3)
		#print(ass)
		#if (data =="bli"):
			#blink2()
			#conn.send("ready")
		 

timeout = 0    
if __name__ == '__main__':
	
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()
    print("Waiting for connection")
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
        conn.send("ready")
        while True:
            try:
                data = conn.recv(3)
            except socket_error,e:
                dead = True
                print(e)
                pass

            if(data=="sto"):
                print("connection closed")
                
                conn.close()
                blink(black)
                strip.show()
                conn, addr = s.accept()           
            if(data== "led"):
                a=scrollaus()
                if(a== True):
                    print(a)
                    socketisded();
                conn.send("ready")
            if (data =="bli"):
                blink2()
                conn.send("ready")
            if (data =="rai"):
                a= rainbow(strip)
                if(a == True):
					socketisded()
					print("asd")
                if(a == False):
                    print(a)
                    try:
						conn.send("ready")
                    except socket_error,e:
                        print(e)
    except KeyboardInterrupt:
        if args.clear:
            conn.close()
            blink2(black)
            
                
