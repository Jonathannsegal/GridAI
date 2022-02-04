"""Imports"""
import requests

resp = requests.post("localhost:50000", files={'file': open('eight.png', 'rb')})

print(resp.json())
