import requests
import json
url = "https://api.assemblyai.com/v2/realtime/b2e3c6c71d450589b2f4f0bb1ac4efd2d5e55b1f926e552e02fc0cc070eaedbd"
# url = "wss://api.assemblyai.com/v2/realtime/ws"

payload = json.dumps({
    "data": {"expires_in": 360000},

})
headers = {
  'Content-Type': 'application/json',
  'Access-Control-Request-Headers': '*',
  'api-key': 'd22c276f81de4a55bc9301fb3a54f839',
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
