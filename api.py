import requests
import json
url = "https://ap-south-1.aws.data.mongodb-api.com/app/data-abcxa/endpoint/data/v1/action/insertOne"

payload = json.dumps({
    "collection": "BBOT",
    "database": "Techboys",
    "dataSource": "Cluster0",
    "document": {
        "_id": 1,
        "key": "user",
        "value": "Hello, i'm using API to connect with you!"
    }
})
headers = {
  'Content-Type': 'application/json',
  'Access-Control-Request-Headers': '*',
  'api-key': 'sC6c0nsPlmQuKYQOMrFmm2YCF52kFIUVKTC0J3Hzim6dXGeREuX9Kb0a6MectYed',
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
