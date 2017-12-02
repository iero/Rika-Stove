import sys
import time
import requests

# import json
# import urllib2

import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup # parse page

def connect(client, url_base, url_login, url_stove, user, pwd) :
	data = {
		'email':user,
		'password':pwd}

	r = client.post(url_base+url_login, data)
	# print(r.url)
	# print(r.text)

	if ('Log out' in r.text) == True :
		print('Connected to Rika Firenet')

		soup = BeautifulSoup(r.content, "html.parser")
		text = soup.find("ul", {"id": "stoveList"})
		# print(text)
		if text is not None :
			stoveName = text.find('a').text
			a = text.find('a', href=True)
			stove = a['href'].replace(url_stove,'')
			print("Found the Stove : {} [{}]".format(stoveName,stove))
			return stove

	return ""

def set_stove_temperature(client, url_base, url_api, stove, temperature) :
	# Security : Do not set extreme values
	min = 14
	max = 24

	if min <= temperature <= max :
		cmd = '&targetTemperature='+str(temperature)
		actual = get_stove_informations(client, url_base, url_api, stove)
		data = actual['controls']
		data['targetTemperature'] = str(temperature)

		r = client.post(url_base+url_api+stove+'/controls', data)
		# print(r.url)
		if ('OK' in r.text) == True :
			print('Temperature target is now {} degC'.format(temperature))
			return True

def get_stove_informations(client, url_base, url_api, stove) :
	r = client.get(url_base+url_api+stove+'/status?nocache=')
	return r.json()

def show_stove_informations(data) :

	print("+ Stove {0} [{1}]".format(data['name'],data['stoveID']))
	print("+- Last seen {} min ago".format(data['lastSeenMinutes']))
	lastConfirmedRevision = time.strftime('%d/%m/%Y %H:%M', time.localtime(data['lastConfirmedRevision']))
	print("+- Last Revision : {}".format(lastConfirmedRevision))

	# 'controls' available :
	#'revision': 1511463447, 'onOff': True, 'operatingMode': 2, 'heatingPower': 70, 'targetTemperature': 18, 'heatingTimesActive': False, 'heatingTimesActiveForComfort': False, 'setBackTemperature': 13, 'convectionFan1Active': False, 'convectionFan1Level': 0, 'convectionFan1Area': 0, 'convectionFan2Active': False, 'convectionFan2Level': 0, 'convectionFan2Area': 0, 'frostProtectionActive': False, 'frostProtectionTemperature': 4

	print("\n+- Control : ")
	revision = time.strftime('%d/%m/%Y %H:%M', time.localtime(data['controls']['revision']))
	print("+-- Last Revision : {}".format(revision))

	if data['controls']['onOff'] :
		print("+-- Stove is online")
	else :
		print("+-- Stove is offline")

	if data['controls']['operatingMode'] == 0 :
		print("+-- Operating mode : Manual with {}% power".format(data['controls']['heatingPower']))
	elif data['controls']['operatingMode'] == 1 :
		print("+-- Operating mode : Automatic with {}% power".format(data['controls']['heatingPower']))
	elif data['controls']['operatingMode'] == 2 :
		print("+-- Operating mode : Comfort with {}% power".format(data['controls']['heatingPower']))

	print("+-- Target Temperature : {} degC".format(data['controls']['targetTemperature']))
	print("+-- Protection Temperature : {} degC".format(data['controls']['setBackTemperature']))

	# 'sensors' available :
	#'statusError': 0, 'statusWarning': 0, 'statusService': 0, 'statusMainState': 4, 'statusSubState': 3, 'statusFrostStarted': False, 'inputFlameTemperature': 414, 'inputRoomTemperature': 17, 'inputExternalRequest': True, 'outputDischargeMotor': 391, 'outputInsertionMotor': 0, 'outputIDFan': 1368, 'outputAirFlaps': 0, 'outputIgnition': False, 'parameterStoveTypeNumber': 14, 'parameterVersionMainBoard': 223, 'parameterVersionTFT': 223, 'parameterRuntimePellets': 267, 'parameterRuntimeLogs': 0, 'parameterFeedRateTotal': 257, 'parameterFeedRateService': 443, 'parameterOnOffCycles': 9}, 'stoveType': 'CORSO', 'stoveFeatures': {'multiAir1': False, 'multiAir2': False, 'insertionMotor': False, 'airFlaps': False, 'logRuntime': False}}

	print("\n+- Sensors : ")
	if data['sensors']['statusMainState'] == 1 :
		if data['sensors']['statusSubState'] == 0 :
			print("+-- Stove off")
		elif data['sensors']['statusSubState'] == 1 or data['sensors']['statusSubState'] == 3:
			print("+-- Stove standby")
		elif data['sensors']['statusSubState'] == 2 :
			print("+-- External command")
		else :
			print("+-- Unknown State")
	elif data['sensors']['statusMainState'] == 2 :
		print("+-- Stove Waking up")
	elif data['sensors']['statusMainState'] == 3 :
		print("+-- Stove Starting")
	elif data['sensors']['statusMainState'] == 4 :
		print("+-- Stove burning (control mode)")
	elif data['sensors']['statusMainState'] == 5 :
		if data['sensors']['statusSubState'] == 3 or data['sensors']['statusSubState'] == 4 :
			print("+-- Stove deep cleaning")
		else :
			print("+-- Stove cleaning")
	elif data['sensors']['statusMainState'] == 6 :
		print("+-- Stove burn off")
	else :
		print("+-- Unknown Stove state")

	print("+-- Room Temperature : {} degC".format(data['sensors']['inputRoomTemperature']))
	print("+-- Flame Temperature : {} degC".format(data['sensors']['inputFlameTemperature']))

	print("+-- Pellets consumption : {0} Kg ({1} h)".format(
		data['sensors']['parameterFeedRateTotal'],
		data['sensors']['parameterRuntimePellets']))

	print("+-- Diag Motor : {} %o".format(data['sensors']['outputDischargeMotor']))
	print("+-- Fan velcity : {} rps".format(data['sensors']['outputIDFan']))

def get_stove_consumption(data) :
	return data['sensors']['parameterFeedRateTotal']

def is_stove_burning(data) :
	if data['sensors']['statusMainState'] == 4 or data['sensors']['statusMainState'] == 5 :
		return True
	else :
		return False

def updateSensor(domoticz,idx,value) :
		if (value is None) : return
		client = requests.session()
		url="http://"+domoticz+"/json.htm?type=command&param=udevice&idx="+str(idx)+"&nvalue=0&svalue="+str(value)+";0"
		# json.load(urllib2.urlopen(url))
		r = client.get(url)
		print(r.url)
		return

if __name__ == "__main__":

	if len(sys.argv) < 2 :
		print(u"Please use # python rika.py cmd [val]")
		print(u"Cmd can be :")
		print(u"+ get [status|pellet]")
		print(u"+ set temperature")
		print(u"+ push -- to domoticz")
		sys.exit(1)

	auth_tree = ET.parse("settings.xml")
	auth_root = auth_tree.getroot()

	for service in auth_root.findall('service') :
		if service.get("name") == "firenet" :
			user = service.find('user').text
			pwd = service.find('password').text

			url_base = service.find('url_base').text
			url_login = service.find('url_login').text
			url_stove = service.find('url_stove').text
			url_api = service.find('url_api').text

		if service.get("name") == "domoticz" :
			dmz_server = service.find('server').text
			dmz_burning = service.find('pellets').text
			dmz_pellets = service.find('pellets').text
			dmz_target_temp = service.find('target_temp').text
			dmz_room_temp = service.find('room_temp').text

	client = requests.session()
	stove = connect(client, url_base, url_login, url_stove, user, pwd)

	if len(stove) == 0 :
		print("No stove found (connection failed ?)")
		sys.exit(1)

	if sys.argv[1] == 'get' :
		stove_infos = get_stove_informations(client, url_base, url_api, stove)
		if len(sys.argv) >= 3 :
			if sys.argv[2] == 'status' :
				print("+-- Stove on : {0}".format(is_stove_burning(stove_infos)))
			elif sys.argv[1] == 'pellets' :
				print("+-- Pellets consumption : {0} Kg".format(get_stove_consumption(stove_infos)))
		else :
			show_stove_informations(stove_infos)

	if sys.argv[1] == 'update' :
		stove_infos = get_stove_informations(client, url_base, url_api, stove)
		updateSensor(dmz_server,dmz_pellets,get_stove_consumption(stove_infos))


	if sys.argv[1] == 'set' and len(sys.argv) > 2 :
		set_stove_temperature(client, url_base, url_api, stove, int(sys.argv[2]))
