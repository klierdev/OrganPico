# OrganPico
A not so useful remote MIDI organ controller using Pico W 

## What it is
It's a self hosting website running on an access point which is all powered by the Raspberry Pi Pico (2) W. 
When you click/hold a button on the web gui it will then send a midi signal to GrandOrgue (Or Hauptwerk/Sweelinq, but not tested)
**It's very simple and it really isn't that useful since there is a massive delay in the HTTP traffic, but still fun :).**

![Screenshot of the web gui](https://github.com/klierdev/OrganPico/blob/main/Screenshots/WebGui.png?raw=true)



## How to set it up:

![Photo of Pico W](https://raw.githubusercontent.com/klierdev/OrganPico/refs/heads/main/Screenshots/PicoW.jfif?raw=true)

- Get a Raspberry Pi Pico W (2 W probably works too, but it must be a W since it has Wi-Fi capabilities)

- [Download the CircuitPython](https://circuitpython.org/downloads) .uf2 file for your microcontroller: 


- First hold the button, THEN plug the Pico into your computer. -> There should be popping up an external drive on your computer, something called RP2 or similar. [Follow this guide](https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython/circuitpython)


![Photo of external drives](https://github.com/klierdev/OrganPico/blob/main/Screenshots/Drives.png?raw=true)
- Drag and drop the Circuit Python .uf2 file into the external drive of the Pico. It should restart the Pico and start with circuitpython and the drive should be called "CIRCUITPY".


![Photo of installed libraries](https://github.com/klierdev/OrganPico/blob/main/Screenshots/Libraries.png?raw=true)
- Download the Adafruit CircuitPython Bundle, it contains libraries which we need. https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases/
- Extract the .zip file (Using 7 zip or whatever) and copy the following folders into the 'lib' folder of the CIRCUITPY drive:
   - adafruit_httpserver
   - adafruit_midi
   - adafruit_wsgi

- After that replace the code.py from the CIRCUITPY drive with the [code.py](https://github.com/klierdev/OrganPico/blob/main/code.py) file from this repository:
- Now navigate connect to the Wi-Fi access point and go to your browser and go to http://192.168.4.1 and it should work.

![Photo of MIDI settings in GrandOrgue](https://github.com/klierdev/OrganPico/blob/main/Screenshots/MidiSettings_GrandOrgue.png)
- (Optional) If you don't hear any sound it's probably because you didn't (properly) configure GrandOrgue. Right click on a random key on the GrandOrgue keyboard and a window should popup.
- Click on "Listen for Event" on GrandOrgue and then click on a random key on the [Web Gui](http://192.168.4.1).


## Credits
- Me
- deepseek (I tried GPT-4o and it was terrible, deepseek still had many errors though)

Use VSCode with this extension if you want to modify the code: https://marketplace.visualstudio.com/items?itemName=joedevivo.vscode-circuitpython
Also feel free to open up an issue if you have any question or if you've found bugs. :)
