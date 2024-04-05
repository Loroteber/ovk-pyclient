from win11toast import toast
import os
import requests
from pickle import load
current_dir = os.path.dirname(__file__)
userdata_file = os.path.join(current_dir, "userdata.py")
with open(userdata_file, "rb") as userdata:
	registred = load(userdata)
	token = load(userdata)

date = 0

def service():
	try:
		notification_request = requests.get(url=f'https://ovk.to/method/Notifications.get?access_token={token}&count=1').json()
		if 'response' in notification_request:
			notification = notification_request['response']
			items = notification['items']
			profiles = notification['profiles']
			global date
			if not items:
				service()
			elif date == items[0]['date']:
				service()
			else:
				date = items[0]['date']
				link = {'activationType': 'protocol', 'arguments': 'https://ovk.to/notifications?act=new', 'content': 'Открыть'}
				toast(f'{profiles[0]['first_name']} {profiles[0]['last_name']}', f'will {items[0]['type']}', icon=profiles[0]['photo'], buttons=[link])
				service()
		else:
			toast('Произошла ошибка!', 'При запросе произошла ошибка, связанная с неправильным токеном. Пожалуйста, войдите в клиент снова.')
	except requests.exceptions.ConnectionError:
		toast('Произошла ошибка!', 'Не удаётся подключиться к серверу.')

service()