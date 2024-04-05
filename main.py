# импорт всякой всячины не ну а чё
import os
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


print(f'\n\n{Back.BLUE}{Style.BRIGHT} OpenVK {Style.RESET_ALL}{Back.WHITE}{Fore.BLACK} Python client {Style.RESET_ALL}') # заголовок

def bruuh(): # прогресс невозможен без входа
	print(f'{Style.RESET_ALL}\n{Back.RED}{Style.BRIGHT} Ошибка! {Style.RESET_ALL}\nДля исполнения данной команды требуется вход.\nВведите {Fore.YELLOW}login{Style.RESET_ALL}, чтобы войти.')
	command()

def helpme(): # список команд
	print(f'{Style.RESET_ALL}\nВход не требуется:')
	print(f'{Fore.YELLOW}help{Style.RESET_ALL}		{Style.DIM}выводит этот список{Style.RESET_ALL}')
	print(f'{Fore.YELLOW}login{Style.RESET_ALL}		{Style.DIM}вход в аккаунт{Style.RESET_ALL}')
	print(f'{Fore.YELLOW}exit{Style.RESET_ALL}		{Style.DIM}выход из программы{Style.RESET_ALL}')
	print('\nВход требуется:')
	print(f'{Fore.YELLOW}logout{Style.RESET_ALL}		{Style.DIM}выход из аккаунта{Style.RESET_ALL}')	
	print(f'{Fore.YELLOW}post{Style.RESET_ALL}		{Style.DIM}запостить на своей стене{Style.RESET_ALL}')	
	command()

def main():
	if registred == 0:
		bruuh()
	else:
		try:
			global token
			global email
			global password
			notification_request = requests.get(url=f'https://ovk.to/method/Account.getCounters?access_token={token}').json()
			if 'response' in notification_request:
				notification = notification_request['response']
				print(f'\n{Style.RESET_ALL}{Fore.YELLOW}{name1} {name2}{Style.RESET_ALL}\nНовых...\nУведомлений: {Fore.YELLOW}{notification['notifications']}{Style.RESET_ALL}\nСообщений: {Fore.YELLOW}{notification['messages']}{Style.RESET_ALL}')
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
				print('Произошла ошибка')
				command()
		except requests.exceptions.ConnectionError: 
			print(f'{Style.RESET_ALL}\n{Back.RED}{Style.BRIGHT} Ошибка! {Style.RESET_ALL}\nНе удаётся подключиться к серверу.')
			command()			

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
	elif cmd == 'checker':
		print('Откройте checker.exe (Windows10-11 only, WIP)')
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


