# Rika stove

G. Fabre - 2017

python code to handle Rika stoves.
Need a working firenet account.

### Dependancies

$ pip install beautifulsoup4

### Setup

- Change user and password in settings-example.xml file
- Rename settings-example.xml to settings.xml
- run 'python rika.py'

### Functionalities :

- Get data from your stove (1 stove yet, but can be extended)
- Set temperature to X degrees
- Update sensors values to domoticz
- Control temperature from domoticz

<img src="https://github.com/iero/Rika-Stove/raw/master/misc/dmz_th_pellets.png" width="250">

![](https://github.com/iero/Rika-Stove/raw/master/misc/dmz_pellets.png)

### Domoticz

- Create dummy device 'Rika'
- On this device, create sensors :

![](https://github.com/iero/Rika-Stove/raw/master/misc/dmz_sensors.png)

- Fill idx values in settings file
- Update and place lua file in domoticz/scripts/lua directory

