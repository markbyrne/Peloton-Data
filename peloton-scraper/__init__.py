#!/usr/bin/env python
""":"""

__author__ = "Mark Byrne"
__version__ = "1.0"
__email__ = "MarkByrne.Pro@gmail.com"
__date__ = "20220920"


import requests
import pandas as pd
import os


api_url = "https://api.onepeloton.com"


def get_data(endpoint, payload=None, session=None):
	if session is None:
		session = requests.Session()

	print(f"Getting {endpoint} data...")
	end_point = f"/api/{endpoint}"

	response = session.get(f"{api_url}{end_point}", params=payload)
	print(response)
	if response.status_code < 200 or response.status_code >= 300:
		raise Exception(f"Bad response: {response.status_code}")

	json = response.json()
	print(json)

	try:
		total = json["total"]
	except KeyError:
		total = None

	try:
		if len(json["data"]) > 0:
			data = json["data"]
			print("DATA FLAG FOUND")
		else:
			data = json
			print("DATA FLAG NOT FOUND - Handle data in calling function")
	except KeyError:
		data = json

	try:
		limit = json['limit']
	except KeyError:
		try:
			limit = json['count']
		except KeyError:
			limit = 20

	try:
		pages = json["page_count"]
		print(f"ADDITIONAL {pages} PAGES FOUND")

		for page in range(1, pages):
			print(f"Getting Data from page {page}")
			payload = {"page": page, "limit":  limit}
			response = session.get(f"{api_url}{end_point}", params=payload)
			json = response.json()

			data.extend(json["data"])
		print(f"Got Data from {pages} pages.")
	except KeyError:
		print("PAGE ITERATION UNSUCCESSFUL")
		pass

	if total:
		print(f"Total: {total} | Captured: {len(data)}")
		if total != len(data):
			raise Warning("Not all data seems to have been captured")
	else:
		print(f"Captured: {len(data)}")

	return data


def get_instructors():
	data = get_data("instructor", payload=None)
	df = pd.DataFrame(data)
	df.set_index("id", inplace=True)
	print(df.head(10))

	df.to_csv(path_or_buf=f"../datasets/instructors.csv")


def get_metadata():
	data = get_data("ride/metadata_mappings", payload=None)

	print(data.keys())

	for key, value in data.items():
		print(key, value)
		df = pd.DataFrame(value)

		try:
			df.set_index("id", inplace=True)
			print(df.head(10))
			df.to_csv(path_or_buf=f"../datasets/metadata/{key}-metadata.csv")
		except KeyError:
			print(df.head(10))
			df.to_csv(path_or_buf=f"../datasets/metadata/{key}-metadata.csv", index=False)


def get_workouts(s):
	# {"browse_category": "Cycling"}
	data = get_data("v2/ride/archived", payload={"limit": "100"}, session=s)

	print(data)

	df = pd.DataFrame(data)
	try:
		df.set_index("id", inplace=True)
		print(df.head(10))
		df.to_csv(path_or_buf=f"../datasets/workouts.csv")
	except KeyError:
		print(df.head(10))
		df.to_csv(path_or_buf=f"../datasets/workouts.csv", index=False)


if __name__ == "__main__":
	get_instructors()
	get_metadata()

	s = requests.Session()
	payload = {'username_or_email': os.environ.get('EMAIL'), 'password': os.environ.get('PASS')}
	s.post('https://api.onepeloton.com/auth/login', json=payload)
	print(s.headers)

	get_workouts(s)
