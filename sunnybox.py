import requests
import json
import logging

log = logging.getLogger('')
log.setLevel(logging.DEBUG)

log_format = logging.Formatter('%(asctime)s - %(levelname)-8s - %(message)s')

fh = logging.FileHandler('energy.log')
fh.setFormatter(log_format)
log.addHandler(fh)

log.info("starting")



payload = {
		  "version": "1.0",
		  "proc": "GetPlantOverview",
		  "id": "1",
		  "format": "JSON"
	}

url = 'http://10.1.10.33/rpc'
headers = {'content-type': 'application/json'}
data = 'RPC=%s' % json.dumps(payload)
req = requests.post(url, data=data)

result = req.json()
power = result["result"]["overview"][0]['value']
today = result["result"]["overview"][1]['value']

log.debug("power = %s W" % power)
log.debug("today = %s kW" % today)

with open("keys.json") as fh:
  keys = json.load(fh)


log.info("posting to phant")
r = requests.post(keys["inputUrl"], params = { "now_w": power, "total_today_kw": today, "private_key": keys["privateKey"] })
log.info(r.url)
log.info(r.status_code)
log.info(r.text)


log.info("posting to cursivedata")
datastore_id = 24
key = 'value'
value = power

from post_data import cursive_data
cd = cursive_data(datastore_id)
cd.add_datapoint(key, value)
cd.start()


log.info("done")


