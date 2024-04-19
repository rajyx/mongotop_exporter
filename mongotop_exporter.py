from pymongo import MongoClient
import time

client = MongoClient(host="192.168.1.21", port=27017, username="exporter", password="exporter")
admin_db = client.admin
previous_top = admin_db.command("top")["totals"]
previous_top.pop('note')

time.sleep(5)

next_top = admin_db.command("top")["totals"]
next_top.pop('note')

for collection in previous_top:
    print(f"{collection} {previous_top[collection]['total']}")

print("Try to get next top")

for coll in next_top:
    print(f"{coll} {next_top[coll]['total']}")