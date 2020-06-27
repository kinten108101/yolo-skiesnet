import numpy as np
import json
import io

PATH = "input/imageloader.json"

with io.open(PATH, 'r') as f:
	file = json.load(f, strict=False)
	print(file['object'])


