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
				if items[0]['type'] == 'wall':
					global aa
					aa = f'Пишет на вашей стене'
				elif items[0]['type'] == 'copy_post':
					aa = f'Репостит ваш пост'
				elif items[0]['type'] == 'comment_post':
					aa = f'Комментирует ваш пост'
				elif items[0]['type'] == 'like_post':
					aa = f'Лайкает ваш пост'
				date = items[0]['date']
				link = {'activationType': 'protocol', 'arguments': 'https://ovk.to/notifications?act=new', 'content': 'Открыть'}
				toast(f'{profiles[0]['first_name']} {profiles[0]['last_name']}', f'{aa}', buttons=[link])
				service()
		else:
			toast('Произошла ошибка!', 'При запросе произошла ошибка, связанная с неправильным токеном. Пожалуйста, войдите в клиент снова.')
	except requests.exceptions.ConnectionError:
		toast('Произошла ошибка!', 'Не удаётся подключиться к серверу.')

service()