
import ddf.minim.*;
import ddf.minim.signals.*;
import ddf.minim.analysis.*;
import ddf.minim.effects.*;
import processing.sound.*;
import ddf.minim.analysis.FFT;
import processing.net.*; 
import controlP5.*;

Client myClient;
Minim minim;
AudioPlayer song;
AudioInput in;
ControlP5 cp5; //create ControlP5 object
import processing.serial.*;
import cc.arduino.*;


float specLow = 0.03; // 3%
float specMid = 0.125;  // 12.5%
float specHi = 0.20;   // 20%
float scoreLow = 0;
float scoreMid = 0;
float scoreHi = 0;
float oldScoreLow = scoreLow;
float oldScoreMid = scoreMid;
float oldScoreHi = scoreHi;
float scoreDecreaseRate = 25;



FFT fft;

float kickSize, snareSize, hatSize;
PFont font;
Slider s;
float redslider = 0.15;
float greenslider = 0.15;
float blueslider = 0.15;
boolean toggleValue = false;
void setup() {
    stroke(255);
  strokeWeight(3);
  strokeCap(ROUND);
  size(700, 400);
  cp5 = new ControlP5(this);
  myClient = new Client(this, "192.168.0.9", 5218); //ip address of your raspberry pi
  minim = new Minim(this);
  in = minim.getLineIn( Minim.STEREO, 2048 ); //Microphone input
  fft = new FFT(in.bufferSize(), in.sampleRate());
  font = createFont("calibri light bold", 18);    // custom font for buttons and title

  cp5.addButton("seis")     
    .setPosition(100, 80)  
    .setSize(80, 50)      
    .setFont(font)
  ;   
   cp5.addButton("defaults")     
    .setPosition(600, 0)  
    .setSize(100, 30) 
    .setFont(font)
  ; 
   cp5.addSlider("redslider")

         .setPosition(0,50)
         .setRange(0,1)
         .setValue(0.2)
         .setSize(200,20);
   cp5.addSlider("greenslider")
         .setPosition(0,25)
         .setRange(0,1)
         .setValue(0.2)
         .setSize(200,20);
    cp5.addToggle("toggleValue")
     .setPosition(40,100)
     .setSize(50,20);
   cp5.addSlider("blueslider")
         .setPosition(0,0)
         .setRange(0,1)
         .setValue(0.2)
          .setSize(200,20);
   cp5.addSlider("decreaserate")
         .setPosition(300,0)
         .setRange(0,100)
         .setValue(25)
          .setSize(200,20);
   
   cp5.addSlider("specLow")
         .setPosition(0,140)
         .setRange(0,1)
         .setValue(0.03)
         .setSize(100,20);
   cp5.addSlider("specMid")
         .setPosition(150,140)
         .setRange(0,1)
         .setValue(0.125)
         .setSize(100,20);
   cp5.addSlider("specHi")
         .setPosition(300,140)
         .setRange(0,1)
         .setValue(0.2)
         .setSize(100,20);
   cp5.addButton("blink")
         .setPosition(3,80)
         .setSize(50,20);
         
   cp5.addButton("scroll")
         .setPosition(3,100)
         .setSize(50,20);
   cp5.addButton("T800")
         .setPosition(650,110)
         .setSize(50,20);
   cp5.addButton("karma")
         .setPosition(650,70)
         .setSize(50,20);     
    cp5.addButton("housee")
         .setPosition(650,50)
         .setSize(50,20);
    cp5.addButton("burzum")
         .setPosition(650,30)
         .setSize(50,20);
    cp5.addButton("bass")
         .setPosition(650,90)
         .setSize(50,20);
    cp5.addButton("grb")
         .setPosition(650,200)
         .setSize(50,20);
    cp5.addButton("rgb")
         .setPosition(650,220)
         .setSize(50,20);
    cp5.addButton("brg")
         .setPosition(650,240)
         .setSize(50,20);
    cp5.addButton("gbr")
         .setPosition(600,200)
         .setSize(50,20);
    cp5.addButton("rbg")
         .setPosition(600,220)
         .setSize(50,20);
    cp5.addButton("bgr")
         .setPosition(600,240)
         .setSize(50,20);         
}
String ledi = "led";
String red,green,blue;
String colorscheme = "grb";
float value;
void controlEvent(ControlEvent theEvent){ 
    if(theEvent.getController().getName()=="redslider"){redslider = theEvent.getController().getValue();}
    if(theEvent.getController().getName()=="greenslider"){greenslider = theEvent.getController().getValue();}
    if(theEvent.getController().getName()=="blueslider"){blueslider = theEvent.getController().getValue();}
    if(theEvent.getController().getName()=="specLow"){specLow = theEvent.getController().getValue();}
    if(theEvent.getController().getName()=="specMid"){specMid = theEvent.getController().getValue();}
    if(theEvent.getController().getName()=="decreaserate"){scoreDecreaseRate = theEvent.getController().getValue();}    
    if(theEvent.getController().getName()=="specHi"){specHi = theEvent.getController().getValue();}
    if(theEvent.getController().getName()=="defaults"){
    cp5.getController("blueslider").setValue(0.15);
    cp5.getController("redslider").setValue(0.15);
    cp5.getController("greenslider").setValue(0.15);
    cp5.getController("specLow").setValue(0.03);
    cp5.getController("specMid").setValue(0.12);
    cp5.getController("specHi").setValue(0.22);
    colorscheme = "grb";
  }
    if(theEvent.getController().getName()=="housee"){
    cp5.getController("blueslider").setValue(0.26);
    cp5.getController("redslider").setValue(0.19);
    cp5.getController("greenslider").setValue(0.38);
    cp5.getController("specLow").setValue(0.03);
    cp5.getController("specMid").setValue(0.14);
    cp5.getController("specHi").setValue(0.33);
  }
    if(theEvent.getController().getName()=="bass"){
    cp5.getController("blueslider").setValue(0.14);
    cp5.getController("redslider").setValue(0.15);
    cp5.getController("greenslider").setValue(0.35);
    cp5.getController("specLow").setValue(0.015);
    cp5.getController("specMid").setValue(0.09);
    cp5.getController("specHi").setValue(0.21);
  }
    if(theEvent.getController().getName()=="karma"){
    cp5.getController("blueslider").setValue(0.14);
    cp5.getController("redslider").setValue(0.3);
    cp5.getController("greenslider").setValue(0.6);
    cp5.getController("specLow").setValue(0.02);
    cp5.getController("specMid").setValue(0.09);
    cp5.getController("specHi").setValue(0.21);
    colorscheme = "brg";
  }
    if(theEvent.getController().getName()=="burzum"){
    cp5.getController("blueslider").setValue(0.07);
    cp5.getController("redslider").setValue(0.22);
    cp5.getController("greenslider").setValue(0.37);
    cp5.getController("specLow").setValue(0.02);
    cp5.getController("specMid").setValue(0.14);
    cp5.getController("specHi").setValue(0.26);
    colorscheme = "grb";
  }
    if(theEvent.getController().getName()=="T800"){
    cp5.getController("blueslider").setValue(0.32);
    cp5.getController("redslider").setValue(0.16);
    cp5.getController("greenslider").setValue(0.23);
    cp5.getController("specLow").setValue(0.03);
    cp5.getController("specMid").setValue(0.17);
    cp5.getController("specHi").setValue(0.41);
    colorscheme = "rbg";
  }  
  if(theEvent.getController().getName()=="blink"){ledi = "bli";}
  if(theEvent.getController().getName()=="scroll"){ledi = "led";}
  
  if(theEvent.getController().getName()=="grb"){colorscheme = "grb";}
  if(theEvent.getController().getName()=="rgb"){colorscheme = "rgb";}
  if(theEvent.getController().getName()=="brg"){colorscheme = "brg";}
  if(theEvent.getController().getName()=="gbr"){colorscheme = "gbr";}
  if(theEvent.getController().getName()=="rbg"){colorscheme = "rbg";}
  if(theEvent.getController().getName()=="bgr"){colorscheme = "bgr";}

}

float m, n, j,k,g,h;
void draw() {
  fft.forward(in.mix);
  oldScoreLow = scoreLow;
  oldScoreMid = scoreMid;
  oldScoreHi = scoreHi;


  scoreLow = 0;
  scoreMid = 0;
  scoreHi = 0;
 
 
  for(int i = 0; i < fft.specSize()*specLow; i++)
  {
    scoreLow += fft.getBand(i);
  }
  
  for(int i = (int)(fft.specSize()*specLow); i < fft.specSize()*specMid; i++)
  {
    scoreMid += fft.getBand(i);
  }
  
  for(int i = (int)(fft.specSize()*specMid); i < fft.specSize()*specHi; i++)
  {
    scoreHi += fft.getBand(i);
  }

  if (oldScoreLow > scoreLow) { scoreLow = oldScoreLow - scoreDecreaseRate;}
  if (oldScoreMid > scoreMid) {scoreMid = oldScoreMid - scoreDecreaseRate;}
  if (oldScoreHi > scoreHi) {scoreHi = oldScoreHi - scoreDecreaseRate;}

  j = scoreMid*redslider;  //R
  n = scoreLow*greenslider;//G
  g = scoreHi*blueslider;  //B
  j = constrain(j,0,255);
  n = constrain(n,0,255);
  g = constrain(g,0,255);

if (colorscheme=="grb"){k = int(j);m = int(n);h = int(g);}
if (colorscheme=="rgb"){k = int(n);m = int(j);h = int(g);}
if (colorscheme=="brg"){k = int(j);m = int(g);h = int(n);}
if (colorscheme=="gbr"){k = int(n);m = int(j);h = int(g);}
if (colorscheme=="rbg"){k = int(n);m = int(g);h = int(j);}
if (colorscheme=="bgr"){k = int(g);m = int(j);h = int(n);}

  background(m,k,h);
  if (k <= 100){red = "0"+str(k);}
  if (m <= 100){green = "0"+str(m);}
  if (h <= 100){blue = "0"+str(h);}
  
  if (k <= 0){red = "000";}
  if (m <= 0){green = "000";}
  if (h <= 0){blue = "000";}
  
  if (k < 10 && k>0){red = "00"+str(k);}
  if (m < 10 && m>0){green = "00"+str(m);}
  if (h < 10 && h>0){blue = "00"+str(h);}

  if (k >= 100){red = str(k);}
  if (m >= 100){green = str(m);}
  if (h >= 100){blue = str(h);}
  if(red!= "000"){red = red.substring(0, red.length()-2);}
  if(green!= "000"){green = green.substring(0, green.length()-2);}
  if(blue!= "000"){blue = blue.substring(0, blue.length()-2);}

  if (toggleValue ==true){
    if(scoreLow*0.23 >= 120){ledi = "bli";}
    if(scoreLow*0.23 <= 120){ledi = "led";}
}
  myClient.write(ledi);
  myClient.write(red);
  myClient.write(green);
  myClient.write(blue);
  background(k,m,h);


   for(int i = 0; i < 1025*specLow; i++)
  {  
    if(colorscheme == "grb") stroke(0,255,0);
    if(colorscheme == "rgb") stroke(255,0,0);
    if(colorscheme == "brg") stroke(0,0,255);
    if(colorscheme == "gbr") stroke(0,255,0);
    if(colorscheme == "rbg") stroke(255,0,0);
    if(colorscheme == "bgr") stroke(0,0,255);
    line( i, height, i, height - fft.getBand(i)*4 ); 
  }
  for(int i = int(1025*specLow);  i < 1025*specMid; i++)
  { if(colorscheme == "grb") stroke(255,0,0);
    if(colorscheme == "rgb") stroke(0,255,0);
    if(colorscheme == "brg") stroke(255,0,0);
    if(colorscheme == "gbr") stroke(0,0,255);
    if(colorscheme == "rbg") stroke(0,0,255);
    if(colorscheme == "bgr") stroke(0,255,0);
    line( i, height, i, height - fft.getBand(i)*4 ); 
  }
  for(int i = int(1025*specMid); i < 1025*specHi; i++)
  { if(colorscheme == "grb") stroke(0,0,255);
    if(colorscheme == "rgb") stroke(0,0,255);
    if(colorscheme == "brg") stroke(0,255,0);
    if(colorscheme == "gbr") stroke(255,0,0);
    if(colorscheme == "rbg") stroke(0,255,0);
    if(colorscheme == "bgr") stroke(255,0,0);
    line( i, height, i, height - fft.getBand(i)*4 ); 
  }
  for(int i = int(1025*specHi); i < 1025; i++)
  {  stroke(255);
    line( i, height, i, height - fft.getBand(i)*4 ); 
  }
  textSize(24);
  text(red,0,180);
  text(scoreLow*0.23,0,210);
  text(green,150,180);
  text(blue,300,180);
}
void seis() {
  myClient.write("sto");
  myClient.stop();
}
void stop() {
  minim.stop();
  super.stop();
}
  