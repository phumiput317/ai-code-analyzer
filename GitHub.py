import requests
import base64

owner = "phumiput317"
repo = "HW03-65123317"
file_path = "login.dart"

url = f"https://api.github.com/repos/phumiput317/HW03-65123317/contents/login.dart"

response = requests.get(url)

print("Status Code:", response.status_code)

if response.status_code == 200:
    data = response.json()

    content = base64.b64decode(data["content"]).decode("utf-8")

    print("\n===== FILE:", file_path, "=====\n")
    print(content)

else:
    print("FAIL: Cannot read file")
    print(response.text)