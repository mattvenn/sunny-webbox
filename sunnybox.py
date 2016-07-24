import requests
import json
import logging

logging.basicConfig(filename="energy.log", level=logging.DEBUG)

payload = {
		  "version": "1.0",
		  "proc": "GetPlantOverview",
		  "id": "1",
		  "format": "JSON"
	}

url = 'http://185.80.84.74/rpc'
headers = {'content-type': 'application/json'}
data = 'RPC=%s' % json.dumps(payload)
req = requests.post(url, data=data)

result = req.json()
power = result["result"]["overview"][0]['value']
today = result["result"]["overview"][1]['value']

logging.debug("power = %s W" % power)
logging.debug("today = %s kW" % today)

with open("keys.json") as fh:
  keys = json.load(fh)


logging.info("posting to phant")
r = requests.post(keys["inputUrl"], params = { "now_w": power, "total_today_kw": today, "private_key": keys["privateKey"] })
logging.info(r.url)
logging.info(r.status_code)
logging.info(r.text)


logging.info("posting to cursivedata")
datastore_id = 24
key = 'value'
value = power

from post_data import cursive_data
cd = cursive_data(datastore_id)
cd.add_datapoint(key, value)
cd.start()


logging.info("done")


