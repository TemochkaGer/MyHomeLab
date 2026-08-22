import webbrowser
import requests

site = requests.get("https://www.arkto.ru/")
print(site.text)
print(site.status_code)