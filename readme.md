# Rika stove

G. Fabre - 2017

python code to handle Rika stoves.
Need a working firenet account.

### Setup

- Change user and password in settings-example.xml file
- Rename settings-example.xml to settings.xml
- run 'python rika.py'

### Functionalities :

- Get data from your stove (1 stove yet, but can be extended)
- Set temperature to X degrees

- Todo : Will push informations to domoticz

### Domoticz

- Create dummy device 'Rika'
- On this device, create sensors :

![alt text](https://github.com/iero/Rika-Stove/raw/master/misc/dmz_sensors.png)

- Fill idx values in settings file

