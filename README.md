# Audioreactive ws2812b with Raspberry pi
## Why
My goal was to visualize music somehow and lighten up my table. I didn't want to use my raspberry pi to do any actual heavy calculations so I could use it for other purposes too so I made my PC to do all the work and just send the data required over wifi.


## Install the ws281x library
This library is required for controlling the PWM of the GPIO pins
```
sudo apt-get install build-essential python-dev git scons swig
git clone https://github.com/jgarff/rpi_ws281x.git
cd rpi_ws281x
scons
cd python
sudo python setup.py install
```

## Audio configuration
This program was made for visualizing music but you can just use your microphone as input if you like.

This is what we want
![](https://github.com/santniem/raspi_audioreactive_leds/blob/master/images/audio-source.png)
To get your system sound as your microphone input you will need to install [Voicemeeter](https://www.vb-audio.com/Voicemeeter/).
#### Windows sound settings
![](https://github.com/santniem/raspi_audioreactive_leds/blob/master/images/sound-settings.png)

#### Voicemeeter settings
![](https://github.com/santniem/raspi_audioreactive_leds/blob/master/images/voicemeeter-settings.png)

## Running the programs
First you need to start the RaspiRGB.py

```
cd yourinstallationfolder
sudo python RaspiRGB.py
```

After that you can start the RaspiLED.pde using [Processing](https://processing.org/download/).
You have to change the ip addresses on the scripts first thought.

![](https://github.com/santniem/raspi_audioreactive_leds/blob/master/images/giphy.gif)
