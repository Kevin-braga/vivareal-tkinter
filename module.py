import pyodbc, json, requests, time, uuid, random
from bs4 import BeautifulSoup
from PIL import Image
from antigate import AntiGate , AntiGateError


key = "d686bdfeaa9a58be65ffb4c2d0596397"

def get_free_proxies():

	page = requests.get('https://free-proxy-list.net/', headers={'User-Agent':'Mozilla/5.0'})

	soup = BeautifulSoup(page.text,"lxml")

	proxies = soup.select("tbody tr")

	while True:

		proxy = [item.text for item in random.choice(proxies).select("td")[:2]]

		proxy = ':'.join(proxy)

		try:
			r = requests.get("https://www.google.com/", proxies={"https": proxy}, timeout=5)

			if r.status_code == 200: 
				print(proxy)
				return proxy

		except:
			pass

def get_free_proxies_2():

	lista = ['45.167.28.193:8080',
		'186.235.78.212:8080',
		'168.227.54.10:8080',
		'191.242.230.135:8080',
		'131.0.160.150:8080',
		'177.184.63.108:8080',
		'177.125.62.26:3128',
		'187.45.151.191:8080',
		'45.70.106.31:8080',
		' 177.8.216.106:8080',
		' 45.224.173.254:8080',
		' 45.224.44.15:8080',
		' 189.111.249.98:8080',
		' 187.69.89.17:8080',
		' 191.7.20.134:3128',
		' 177.71.77.202:20183',
		' 192.140.28.69:8080',
		' 186.237.221.25:8080',
		' 187.16.137.98:8080',
		' 201.150.54.184:8080',
		' 45.230.78.181:8080',
		' 168.181.196.71:8080',
		' 138.97.97.238:8080',
		' 187.16.4.108:8080',
		' 177.185.151.101:8080',
		' 177.22.203.59:3128',
		' 177.89.85.213:8080',
		' 177.92.244.158:8080',
		' 177.44.82.232:8080',
		' 192.141.12.70:8080',
		'138.68.243.126:8080',
		'68.183.99.243:80',
		'134.209.123.111:8080',
		'142.93.121.254:8080',
		'165.227.180.100:3128',
		'134.209.218.75:8080',
		'134.209.41.247:3128',
		'178.128.65.42:8080',
		'134.209.115.104:3128',
		'45.55.27.161:8080',
		'192.34.63.54:3128',
		'3.95.193.173:80',
		'134.209.45.249:8080',
		'67.205.174.209:3128',
		'165.227.62.167:80',
		'68.110.172.76:3128',
		'68.183.137.143:8080',
		'162.243.108.161:8080',
		'134.209.66.166:8080',
		'104.248.190.115:8080',
		'104.236.54.196:808',
		'155.186.173.52:53281',
		'104.198.232.184:80',
		'104.43.244.233:80',
		'54.71.56.180:80',
		'157.230.80.42:80',
		'45.33.31.25:80	',
		'173.91.0.31:80	',
		'216.75.113.182:39602',
		'74.208.177.198:8',
		'45.63.11.151:8118',
		'38.21.38.6:35458',
		'208.98.186.80:53630',
		'4.34.50.189:55656',
		'162.223.89.92:8080',
		'50.197.38.230:60724',
		'52.124.6.146:40834',
		'24.227.222.69:53281',
		'104.42.155.88:80',
		'52.86.193.247:8080']
	
	lista = list(dict.fromkeys(lista))

	while True:

		proxy = random.choice(lista)

		print("Testando: ", proxy)

		try:
			r = requests.get("https://www.vivareal.com.br/", proxies={"https": proxy}, timeout=5)

			if r.status_code == 200: 
				print("Conseguiu com o proxy: ", proxy)
				return proxy

		except:
			pass	

def get_connection():

	return pyodbc.connect('DRIVER=SQL Server;PORT=1433;SERVER=10.25.0.196;DATABASE=DB_JIVE_2017;UID=jivesa;PWD=J1v3@2017*;Trusted_connection=no')
	
def sql(banco, cursor, tabela, campos, valores):

	valores = ["'{0}'".format(v) for v in valores]

	try:
		query = """INSERT INTO DB_JIVE_2017.DBO.{0} ({1}) VALUES ({2})""".format( tabela, ','.join(campos), ",".join(valores))
		cursor.execute(query)
		banco.commit()

	except pyodbc.Error as error:
		
		print(error)
		#from modules import _email
		#logger.error("<ERROR: %s [%s]>"%(error, documento))
		#_email.send("CELESC",error,documento)

def rest(url, data):

	# Eg. User name="admin", Password="admin" for this code sample.
	usuario = 'admin'
	password = 'jive@2017'

	# Set proper headers
	headers = {"Content-Type":"application/json","Accept":"application/json"}

	data = json.dumps(data)

	# Do the HTTP request
	response = requests.post(url, auth=(usuario, password), headers=headers ,data=data)

	# Check for HTTP codes other than 200
	if response.status_code == 400: 
	    print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
	    exit()


def print_element(img,driver):

	#RANDOM FILENAME
	filename = str(uuid.uuid4()) + ".png"

	driver.save_screenshot(filename)

	location = img.location
	size = img.size
	im = Image.open(filename)
	left = location['x']
	top = location['y']
	right = location['x'] + size['width']
	bottom = location['y'] + size['height']
	im = im.crop((left,top,right,bottom))
	im.save(filename)

	return filename

def digitar_captcha():

	### essa função é usada para testar captchas, não usar em produção
	answer = input("Digite o captcha: \n")
	return (answer)

def solve_captcha(img):
	
	while True:
		try:
			gate = AntiGate(key)            
			captcha_id = gate.send(img)
			answer = (gate.get(captcha_id))
			return (answer)

		except AntiGateError as error:
			print(error)
			break

def solve_recaptcha(url,webkey):

	task = {
	"clientKey":key,
	"task":
		{
			"type":"NoCaptchaTaskProxyless",
			"websiteURL":url,
			"websiteKey":webkey
		},
	"softId":0,
	"languagePool":"pt-BR"
	}

	while True:
		r = requests.post('https://api.anti-captcha.com/createTask', json=task)
		data = json.loads(r.text)
		errorId = data.get('errorId')
		if errorId != 0:
			time.sleep(60)
		else:
			break

	taskId = data.get('taskId')
	
	get = {
	"clientKey":key,
	"taskId": taskId
	}

	while True:
		time.sleep(8)
		r = requests.post('https://api.anti-captcha.com/getTaskResult', json=get)
		data = json.loads(r.text)
		if data['status'] == 'processing':
			continue
		elif data['status'] == 'ready':
			captcha_response = (data['solution']['gRecaptchaResponse'])
			return (captcha_response)

if __name__ == "__main__":

	get_free_proxies()
