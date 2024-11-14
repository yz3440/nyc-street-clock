import os
from dotenv import load_dotenv
import psycopg2 as pg

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


print(DATABASE_URL)
conn = pg.connect(os.getenv("DATABASE_URL"))

print(conn)


# SELECT
# 	ocr.id,
#     ocr.panorama_id,
#     ocr.text,
#     ocr.yaw AS "ocr_yaw",
#     ocr.pitch AS "ocr_pitch",
#     ocr.width AS "ocr_width",
#     ocr.height AS "ocr_height",
#     sv.lat,
#     sv.lng,
#     sv.heading,
#     sv.pitch,
#     sv.roll
# FROM
#     "public"."ocrResult" AS ocr
# JOIN
#     "public"."streetview" AS sv ON ocr.panorama_id = sv.panorama_id
# WHERE
#     ocr.text ~ '^\d{3,4}$'
#     AND ocr.text::int BETWEEN 0 AND 2500;


query = """
SELECT
    ocr.id,
    ocr.panorama_id,
    ocr.text,
    ocr.yaw AS "ocr_yaw",
    ocr.pitch AS "ocr_pitch",
    ocr.width AS "ocr_width",
    ocr.height AS "ocr_height",
    sv.lat,
    sv.lng,
    sv.heading,
    sv.pitch,
    sv.roll
FROM
    "public"."ocrResult" AS ocr
JOIN
    "public"."streetview" AS sv ON ocr.panorama_id = sv.panorama_id
WHERE
    LPAD(ocr.text, 4, '0') ~ '^\d{4}$'
    AND LPAD(ocr.text, 4, '0')::int BETWEEN 0 AND 2500
    AND ocr.confidence > 0.9;
"""


cursor = conn.cursor()
cursor.execute(query)

results = cursor.fetchall()

# save to csv
with open("ocr_data.csv", "w") as f:
    import csv

    writer = csv.writer(f)
    writer.writerow(
        [
            "id",
            "panorama_id",
            "text",
            "ocr_yaw",
            "ocr_pitch",
            "ocr_width",
            "ocr_height",
            "lat",
            "lng",
            "heading",
            "pitch",
            "roll",
        ]
    )
    writer.writerows(results)
