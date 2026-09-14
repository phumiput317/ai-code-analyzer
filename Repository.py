import requests

owner = "YOUR_GITHUB_USERNAME"
repo = "YOUR_REPOSITORY"

url = f"https://api.github.com/repos/{owner}/{repo}"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()

    print("Repository:", data["name"])
    print("Description:", data["description"])
    print("Stars:", data["stargazers_count"])
    print("Language:", data["language"])

else:
    print("Error:", response.status_code)