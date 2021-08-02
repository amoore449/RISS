import json

person = '{"name": "Bob", "languages": ["English", "Fench"]}'
person_dict = json.loads(person)

with open('blink.json') as f:
  data = json.load(f)
print(len(data["rightEyesStills"]["Spot"][0]))

# Lid Data
for x in data["rightEyesStills"]["Lid"]:
    print(x["file"])

#Try spot data
spots = []
for x in data["rightEyesStills"]["Spot"]:
    if x.get("file"):
        print(x.get("file"))
    else:
        print("No File Found")
