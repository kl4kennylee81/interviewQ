import requests
import json

header = {'Authorization' : 'Bearer DEMO_TOKEN'}
base_url = 'https://api.clever.com/v1.1/sections'

def html_response(rel_uri):
	request_url = ''.join([base_url, rel_uri])
	api_response = requests.get(request_url, headers = header)
	return api_response.text
	
def average():

	num_of_students = 0
	num_of_sections = 0
	rel_uri = "/v1.1/sections"

	while True:
		json_response = json.loads(html_response(rel_uri))
		data = json_response["data"]

		s,n = reduce(lambda entry, (sum,n): (len(entry["data"]["students"]) + sum,n+1),data)
		
		num_of_students+=s
		num_of_sections+=n

		links_rel_second = json_response["links"][1]["rel"]
		
		if links_rel_second == "next":
			rel_uri = json_response["links"][1]["uri"]
		else:
			break

if __name__ == "__main__":
	avg = average()
	print("Average per section {}".format(avg))