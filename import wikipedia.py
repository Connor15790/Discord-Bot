import wikipedia
import json
import requests
import random

wikipage = wikipedia.page("Elden Ring", auto_suggest=False)
link = wikipage.images
suffixes = (".png", ".jpg")
links = []

for i in link:
    if len(links)<3 and i.endswith(suffixes):
        links.append(i)

print(random.choice(links))