#!/usr/bin/env python
""":"""

__author__ = "Mark Byrne"
__version__ = "1.0"
__email__ = "MarkByrne.Pro@gmail.com"
__date__ = "20220920"


import requests
import pandas as pd


api_url = "https://api.onepeloton.com"


def get_data(endpoint, payload=None):
	print(f"Getting {endpoint} data...")
	end_point = f"/api/{endpoint}"

	response = requests.get(f"{api_url}{end_point}", params=payload)
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
		data = json["data"]
	except KeyError:
		data = json

	try:
		pages = json["page_count"]

		for page in range(1, pages):
			payload = {"page": page, "limit":  json["limit"]}
			response = requests.get(f"{api_url}{end_point}", params=payload)
			json = response.json()

			data.extend(json["data"])

	except KeyError:
		pass

	if total:
		print(f"Total: {total} | Captured: {len(data)}")
		if total != len(data):
			raise Exception("Not all data seems to have been captured")
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
			df.to_csv(path_or_buf=f"../datasets/{key}-metadata.csv")
		except KeyError:
			print(df.head(10))
			df.to_csv(path_or_buf=f"../datasets/{key}-metadata.csv", index=False)


if __name__ == "__main__":
	# get_instructors()
	get_metadata()
