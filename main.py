import requests
from requests import get, post, put
import sys
import os
import pygame

def size(response_my):
    resp = response_my['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['boundedBy']['Envelope']
    lx, ly = map(float, resp['lowerCorner'].split())
    rx, ry = map(float, resp['upperCorner'].split())
    w = abs(rx - lx)
    h = abs(ry - ly)
    return (w, h)

def scope(response_my):
    w, h = size(response_my)
    return w / 3 , h / 3

def position(response_my):
    return response_my['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']



PLACE = 'Ульяновск'.replace(' ', '+')

geocoder_request = "http://geocode-maps.yandex.ru/1.x/?geocode={}&format=json".format(PLACE)
response = get(geocoder_request)

json_response = response.json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
x, y = json_response.split()


w, h = scope(response.json())
map_request = "http://static-maps.yandex.ru/1.x/?ll={},{}&l=sat&spn={},{}&pt={},{}".format(x, y, w , h, x, y)

response=None
response = requests.get(map_request)

map_file = "map.png"
try:
    with open(map_file, "wb") as file:
        file.write(response.content)
except IOError as ex:
    print("Ошибка записи временного файла:", ex)
    sys.exit(2)

pygame.init()
screen = pygame.display.set_mode((600, 450))
screen.blit(pygame.image.load(map_file), (0, 0))
pygame.display.flip()
while pygame.event.wait().type != pygame.QUIT:
    pass
pygame.quit()
os.remove(map_file)
