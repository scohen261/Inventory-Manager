import requests

id = "Some product slug/UUID"
url = f"https://api.sneakersapi.dev/product/{id}"

response = requests.request("GET", url)

print(response.text)

url = "https://api.sneakersapi.dev/search"

querystring = {"query":"Adidas NMD"}

response = requests.request("GET", url, params=querystring)

print (response.text)
