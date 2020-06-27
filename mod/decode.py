import json
PATH_TO_JSON = "google_vision/response.json"

with open(PATH_TO_JSON, 'r') as j:
	file = json.load(j)
	for obj in file["localizedObjectAnnotations"]:
		if obj["name"] == "Person":
			for coord in obj["boundingPoly"]["normalizedVertices"]:
				print(coord["x"], coord["y"])
