# импорт всякой всячины не ну а чё
import os
from tkinter import *
from io import BytesIO
from PIL import Image, ImageTk
from colorama import init
init()
from colorama import Fore, Back, Style
import requests
from pickle import load, dump
current_dir = os.path.dirname(__file__)
userdata_file = os.path.join(current_dir, "userdata.py")

with open(userdata_file, "rb") as userdata:
	registred = load(userdata)
	token = load(userdata)
	name1 = load(userdata)
	name2 = load(userdata)
	aid = load(userdata)
	email = load(userdata)
	password = load(userdata)

aa = 'none'

print(f'\n\n{Back.BLUE}{Style.BRIGHT} OpenVK {Style.RESET_ALL}{Back.WHITE}{Fore.BLACK} Python client {Style.RESET_ALL}') # заголовок

def bruuh(): # прогресс невозможен без входа
	print(f'{Style.RESET_ALL}\n{Back.RED}{Style.BRIGHT} Ошибка! {Style.RESET_ALL}\nДля исполнения данной команды требуется вход.\nВведите {Fore.YELLOW}login{Style.RESET_ALL}, чтобы войти.')
	command()

def helpme(): # список команд
	print(f'{Style.RESET_ALL}\nВход не требуется:')
	print(f'{Fore.YELLOW}help{Style.RESET_ALL}		{Style.DIM}выводит этот список{Style.RESET_ALL}')
	print(f'{Fore.YELLOW}login{Style.RESET_ALL}		{Style.DIM}вход в аккаунт{Style.RESET_ALL}')
	print(f'{Fore.YELLOW}about{Style.RESET_ALL}		{Style.DIM}о клиенте{Style.RESET_ALL}')	
	print(f'{Fore.YELLOW}exit{Style.RESET_ALL}		{Style.DIM}выход из программы{Style.RESET_ALL}')		
	print(f'{Fore.YELLOW}photo{Style.RESET_ALL}		{Style.DIM}выводит окно с последней сохранённой картинкой в коде{Style.RESET_ALL}')
	print('\nВход требуется:')
	print(f'{Fore.YELLOW}logout{Style.RESET_ALL}		{Style.DIM}выход из аккаунта{Style.RESET_ALL}')	
	print(f'{Fore.YELLOW}post{Style.RESET_ALL}		{Style.DIM}запостить на своей стене{Style.RESET_ALL}')
	command()

def photo():
	print(f'\n{Style.RESET_ALL}Пожалуйста, подождите...')
	root = Tk()
	root.title('котлетки')
	response = requests.get(photo_url)
	image = Image.open(BytesIO(response.content))
	photo = ImageTk.PhotoImage(image)
	width = image.width
	height = image.height
	canvas = Canvas(root, width=width, height=height)
	canvas.pack()
	canvas.create_image(0, 0, anchor=NW, image=photo)
	root.mainloop()
	command()

def main():
	if registred == 0:
		bruuh()
	else:
		try:
			global token
			global email
			global password
			global aid
			notification_request = requests.get(url=f'https://ovk.to/method/Account.getCounters?access_token={token}').json()
			if 'response' in notification_request:
				notification = notification_request['response']
				print(f'\n{Style.RESET_ALL}{Fore.YELLOW}{name1} {name2}{Style.RESET_ALL}\nНовых...\nУведомлений: {Fore.YELLOW}{notification['notifications']}{Style.RESET_ALL}\nСообщений: {Fore.YELLOW}{notification['messages']}{Style.RESET_ALL}')
				wall_request = requests.get(url=f'https://ovk.to/method/Wall.get?access_token={token}&count=1&owner_id={aid}').json()
				wall = wall_request['response']
				items = wall['items']
				comments = items[0]['comments']
				likes = items[0]['likes']
				reposts = items[0]['reposts']
				attachements = items[0]['attachments']
				print(f'\nПоследнй пост: "{items[0]['text']}"')
				if attachements and attachements[0].get('type') == 'photo':
					piska = attachements[0]['photo']
					sizes = piska['sizes']
					for item in wall_request["response"]["items"]:
						for attachment in item["attachments"]:
							if attachment["type"] == "photo":
								for size in attachment["photo"]["sizes"]:
									if size["type"] == "UPLOADED_MAXRES":
										global photo_url
										photo_url = size['url']	
										print(f'Введите {Fore.YELLOW}photo{Style.RESET_ALL}, чтобы посмотреть вложение')
					command()
				if notification['notifications'] > 0:
					notification_request = requests.get(url=f'https://ovk.to/method/Notifications.get?access_token={token}&count=1').json()
					notification = notification_request['response']
					items = notification['items']
					profiles = notification['profiles']
					feedback = items[0]['feedback']
					if items[0]['type'] == 'wall':
						global aa
						aa = f'{Fore.YELLOW}пишет{Style.RESET_ALL} на вашей стене'
					elif items[0]['type'] == 'copy_post':
						aa = f'{Fore.YELLOW}репостит{Style.RESET_ALL} ваш пост'
					elif items[0]['type'] == 'comment_post':
						aa = f'{Fore.YELLOW}комментирует{Style.RESET_ALL} ваш пост'
					elif items[0]['type'] == 'like_post':
						aa = f'{Fore.YELLOW}лайкает{Style.RESET_ALL} ваш пост'
					print(f'\nПоследнее уведомление:\n{profiles[0]['first_name']} {profiles[0]['last_name']} {aa}.')
				command()
			else:
				tokenurl = f'https://ovk.to/token?username={email}&password={password}&grant_type=password'
				response = requests.get(url=tokenurl).json()
				if 'access_token' in response:
					token = response['access_token']
					main()
				else:
					print('Произошла ошибка при получении токена. Войдите снова для решения проблемы.')
					command()
		except requests.exceptions.ConnectionError:
			print(f'{Style.RESET_ALL}\n{Back.RED}{Style.BRIGHT} Ошибка! {Style.RESET_ALL}\nНе удаётся подключиться к серверу.')
			command()

def logout(): # выход
	global registred
	if registred == 0:
		bruuh()
	else:
		poka = input(f'\n{Style.RESET_ALL}{Back.MAGENTA}{Style.BRIGHT} Выход из аккаунта {Style.RESET_ALL}\nПродолжаем? (y - да; n - нет): ')
		if poka == 'y':
			registred = 0
			token = 0
			name1 = ''
			name2 = ''
			aid = 0
			email = ''
			password = ''
			with open(userdata_file, "wb") as save:
				dump(registred, save)
				dump(token, save)
				dump(name1, save)
				dump(name2, save)
				dump(aid, save)
				dump(email, save)
				dump(password, save)
			exit()
		elif poka == 'n':
			command()
		else:
			logout()

def login(): # логин
	print(f'\n{Style.RESET_ALL}{Back.RED}{Style.BRIGHT} Внимание! {Style.RESET_ALL}\nПосле входа ни с кем не делитесь копией клиента, которую сейчас используете, так как после входа данные будут храниться в userdata.py\nНажмите Enter для продолжения...')
	input()
	global email
	email = input(f'Введите электронную почту: {Fore.MAGENTA}{Style.BRIGHT}')
	global password
	password = input(f'{Style.RESET_ALL}Введите пароль: {Fore.MAGENTA}{Style.BRIGHT}')
	tokenurl = f'https://ovk.to/token?username={email}&password={password}&grant_type=password'
	try:
		response = requests.get(url=tokenurl).json()
		if 'access_token' in response:
			token = response['access_token']
			print(f'\n{Style.RESET_ALL}{Back.GREEN}{Style.BRIGHT} Успех! {Style.RESET_ALL}\n')
			accountbruh = requests.get(url=f'https://ovk.to/method/Account.getProfileInfo?access_token={token}').json()
			account = accountbruh['response']
			global registred
			global name1
			global name2
			global aid
			registred = 1
			name1 = account['first_name']
			name2 = account['last_name']
			aid = account['id']
			with open(userdata_file, "wb") as save:
				dump(registred, save)
				dump(token, save)
				dump(name1, save)
				dump(name2, save)
				dump(aid, save)
				dump(email, save)
				dump(password, save)
				main()
			command()
		else:
			print(f'{Style.RESET_ALL}\n{Back.RED}{Style.BRIGHT} Ошибка! {Style.RESET_ALL}\nДанные для входа указаны неверно.\nВведите {Fore.YELLOW}login{Style.RESET_ALL}, чтобы поробовать снова')
			command()
	except requests.exceptions.ConnectionError:
		print(f'{Style.RESET_ALL}\n{Back.RED}{Style.BRIGHT} Ошибка! {Style.RESET_ALL}\nНе удаётся подключиться к серверу.\nВведите {Fore.YELLOW}login{Style.RESET_ALL}, чтобы поробовать снова')
		command()

def post():
	if registred == 0:
		bruuh()
	else:
		try:
			post = input(f'{Style.RESET_ALL}\nВведите текст, который хотите запостить: ')
			post1 = input(f'\n"{post}"\nВсё верно? Продолжаем? (y - да; n - нет): ')
			if post1 == 'y':
				global token
				global email
				global password
				global aid
				request = requests.get(url=f'https://ovk.to/method/Wall.post?owner_id={aid}&access_token={token}&message={post}').json()
				if 'error_code' not in request:
					print(f'\n{Style.RESET_ALL}{Back.GREEN}{Style.BRIGHT} Успех! {Style.RESET_ALL}\n')
					command()
				else: 
					tokenurl = f'https://ovk.to/token?username={email}&password={password}&grant_type=password'
					response = requests.get(url=tokenurl).json()
					if 'access_token' in response:
						token = response['access_token']
						print('Повторите попытку. (был сделан перезапрос на токен)')
						post()
					else:
						print('Произошла ошибка при получении токена. Войдите снова для решения проблемы.')
						command()
			elif post1 == 'n':
				command()
			else:
				print('Неизвестный ответ. Засчитано как за "нет".')
				command()
		except requests.exceptions.ConnectionError: 
			print(f'{Style.RESET_ALL}\n{Back.RED}{Style.BRIGHT} Ошибка! {Style.RESET_ALL}\nНе удаётся подключиться к серверу.')
			command()			

photo_url = 'https://astral.express.wf/hentai/80/80d96b5eac9701a8fda3e283e59aa099ac2e3c0c952ae24b084e74f5895588fa4155a83d97ff340c904b8f6a4dba0a70f60ee9df7fad7ba350be9dd931d32a83_cropped/normal.jpeg'



def command(): # распределение комманд, а также её запрос
	cmd = input(f'\n{Fore.GREEN}>> ')
	if cmd == 'exit': # выход
		exit()
	elif cmd == 'login': # логин
		login()
	elif cmd == 'help': # хелп
		helpme()
	elif cmd == 'logout': # выход из аккаунта и выход из приложения
		logout()
	elif cmd == 'main':
		main()
	elif cmd == "post":
		post()
	elif cmd == 'photo':
		photo()
	elif cmd == 'about':
		print(f'\n{Style.RESET_ALL}{Back.BLUE}{Style.BRIGHT} OpenVK {Style.RESET_ALL}{Back.WHITE}{Fore.BLACK} Python client {Style.RESET_ALL}\n\nНеоффициальный клиент для сайта OpenVK, основанный на языке программирования Python.\n\nТекущая версия: {Fore.YELLOW}0.1{Style.RESET_ALL}\n\nhttps://github.com/Loroteber/ovk-pyclient\nhttps://t.me/loroteber\n\n\nБлагодарим за использование клиента! {Back.RED}{Style.BRIGHT} <3 {Style.RESET_ALL}')
		command()
	else: # юзер ляпнул что-то лишнее
		print(f'{Style.RESET_ALL}\n{Back.RED}{Style.BRIGHT} Ошибка! {Style.RESET_ALL}\nНеизвестная команда!\nВведите {Fore.YELLOW}help{Style.RESET_ALL}, чтобы получить список команд.')
		command()

# проверка на вход
if registred == 0: # инфа о входе отсутвует, приветствуем новичка
	print(f'\nПривет! Я являюсь клиентом для OpenVK и подобных инстансов!\nДля использования клиента необходимо войти.\nДля входа введите {Fore.YELLOW}login{Style.RESET_ALL}.\nДля выхода введите {Fore.YELLOW}exit{Style.RESET_ALL}.')
	command()
else: # инфа о входе имеется, кидаем на главную
	main()
	command()


