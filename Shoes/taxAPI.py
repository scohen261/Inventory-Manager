import requests

zip_code = '70118'
api_url = 'https://api.api-ninjas.com/v1/salestax?zip_code={}'.format(zip_code)
response = requests.get(api_url, headers={'X-Api-Key': 'NYsXWV2Yk4JoLQIpda/lXw==MjudBjgujAQ76mEG'})
if response.status_code == requests.codes.ok:
    print(response.text)
else:
    print("Error:", response.status_code, response.text)
