import json
import re
import os

logfile = "/home/plex/Documents/Scripts/TemperatureFlat/log.json"
keepcharacters = ('.','_','-')

jsonArrayRaw = json.loads(open(logfile).read())
jsonArrayFinal = {
	'temperature': {},
	'humidity': {}
}


for x in jsonArrayRaw:
	# sanitize array key
	currentKeyRaw = (x['model'] + "_" + str(x['id'])).lower()
	currentKey = "".join([c for c in currentKeyRaw if re.match(r'\w', c) or c in keepcharacters])

	baseArray = {
		'model': x['model'],
		'id': x['id'],
	}

	# get temperature and convert to celsius if necessary
	tmp_temperature_C = None

	if 'temperature_C' in x:
		tmp_temperature_C = x['temperature_C']
	elif 'temperature_F' in x:
		tmp_temperature_C = (x['temperature_F'] - 32) / 1.8


	# fill final array
	if tmp_temperature_C:
		tmpTemperature = baseArray.copy()
		tmpTemperature['value'] = float(round(tmp_temperature_C,1))

		# push tmp to final
		jsonArrayFinal['temperature'][currentKey] = tmpTemperature


	# set humidity if possible
	if 'humidity' in x:
		tmpHumidity = baseArray.copy()
		tmpHumidity['value'] = x['humidity']

		# push tmp to final
		jsonArrayFinal['humidity'][currentKey] = tmpHumidity


# print(jsonArrayFinal);

for x in jsonArrayFinal:
	currentUberArray = jsonArrayFinal[x]
	for y in currentUberArray:
		currentArray = currentUberArray[y]
		curlCmd = "curl -i -XPOST \"http://localhost:8086/write?db=HomeLogs\" --data-binary \"flat" + x.capitalize() + ",model=" + currentArray['model'] + ",id=" + str(currentArray['id']) + " value=" + str(currentArray['value']) + "\""
		# print(curlCmd)
		os.system(curlCmd)
