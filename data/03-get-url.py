# randomly select a file in "digits" dir
import os
import random
import csv
from dataclasses import dataclass

files = os.listdir("digits")
random_file = random.choice(files)


print("picked file:", random_file)


@dataclass
class OcrData:
    id: int
    panorama_id: str
    text: str
    ocr_yaw: float
    ocr_pitch: float
    ocr_width: float
    ocr_height: float
    lat: float
    lng: float
    heading: float
    pitch: float
    roll: float


ocr_data = []

with open(f"digits/{random_file}", "r") as f:
    reader = csv.reader(f)
    next(reader)  # skip the header
    for row in reader:
        ocr_data.append(OcrData(*row))


# randomly select one ocr data
random_ocr_data = random.choice(ocr_data)

import utils

gsv_prop = utils.get_google_streetview_props(
    random_ocr_data.panorama_id,
    float(random_ocr_data.lat),
    float(random_ocr_data.lng),
    float(random_ocr_data.ocr_yaw),
    float(random_ocr_data.ocr_pitch),
    float(random_ocr_data.heading),
    float(random_ocr_data.pitch),
    float(random_ocr_data.roll),
    float(random_ocr_data.ocr_width),
    float(random_ocr_data.ocr_height),
)
url = utils.get_google_streetview_url(gsv_prop)
print(url)
