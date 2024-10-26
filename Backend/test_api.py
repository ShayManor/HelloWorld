import requests

# Define the URL and data
url = "http://127.0.0.1:5000/solve"
data = {
    "problem": "x + 4 = 7",
    "solution": "x = 3"
}

# Make the PUT request
response = requests.put(url, json=data)

# Check the response
if response.status_code == 200:
    print("Success:", response.json())
else:
    print("Failed:", response.status_code, response.text)
