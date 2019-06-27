from tkinter import *
from tkinter import filedialog
from PIL import ImageTk
import tkinter.messagebox
import sys ,os ,time ,requests ,json ,yaml ,datetime
import pandas as pd
import numpy as np

### Funções
def get_random_ua():
		random_ua = ''
		ua_file = 'user_agents.txt'
		try:
			with open(ua_file) as f:
				lines = f.readlines()
			if len(lines) > 0:
				prng = np.random.RandomState()
				index = prng.permutation(len(lines) - 1)
				idx = np.asarray(index, dtype=np.integer)[0]
				random_proxy = lines[int(idx)]
		except Exception as ex:
			print('Exception in random_ua')
			print(str(ex))
		finally:
			return random_ua

def tira_c(string):
	try:
		s = string.split("[")[1].split("]")[0]
		return s
	except:
		return string

def numerico(x):
	try:
		return int(x)
	except:
		return 0

def streetnum(x):
	try:
		return str(int(x))
	except:
		return ""

def street2(x):
	try:
		return str(x)
	except:
		return ""

def traduzir(string):
	if string == "SALE":
		string = "VENDA"
	if string == "RENTAL":
		string = "ALUGUEL"
	if string == "SALE,RENTAL":
		string = "VENDA E ALUGUEL"
	if string == "SALE,SALE":
		string = "VENDA"
	if string == "RENTAL,SALE":
		string = "VENDA E ALUGUEL"
	if string == "APARTMENT":
		string = "APARTAMENTO"
	if string == "CONDOMINIUM":
		string = "CASA DE CONDOMINIO"
	if string == "OFFICE":
		string = "SALA COMERCIAL"
	if string == "RESIDENTIAL_ALLOTMENT_LAND":
		string = "LOTE/TERRENO"
	if string == "PENTHOUSE":
		string = "COBERTURA"
	if string == "STORE":
		string = "LOJA"
	if string == "HOME":
		string = "CASA"
	if string == "TWO_STORY_HOUSE":
		string = "SOBRADO"
	if string == "COMMERCIAL_PROPERTY":
		string = "IMÓVEL COMERCIAL"
	return string


class Menu(object):

	def __init__(self):

		self.root = Tk()
		self.root.title("Viva Real")
		self.root.iconbitmap(default='assets/logo.ico')
		self.root.geometry('{}x{}'.format('500', '600'))

		title = Label(self.root, text="Coletador de amostras", font=("Arial Black",12))
		title.grid(row=0,column=0)

		self.folder_icon = ImageTk.PhotoImage(file="assets/folder.png")
		folder_button = Button(self.root, command=self.choose_directory)
		folder_button.config(image=self.folder_icon)
		folder_button.grid(row=0,column=1)

		_help = Button(self.root, text = "?", command=self.ajuda, width=3, bg="gold")
		_help.grid(row=0,column=2)

		####### MID ########

		title_2 = Label(self.root, text="Pesquise a cidade")
		title_2.grid(row=1,column=0)

		search_field = Entry(self.root, width=40)
		search_field.grid(row=4,column=0)

		self.search_icon = ImageTk.PhotoImage(file="assets/PLUS.png")
		search_button = Button(self.root, command= lambda: self.search(search_field.get()))
		search_button.config(image=self.search_icon)
		search_button.grid(row=4,column=1)

		####### BOT ########
		self.button_rodar = Button(self.root, text = "Rodar", bg="white", command=self.run)
		self.button_rodar.place(relx=0.5, rely=0.8,anchor=CENTER, width=80)

	def ajuda(self):
		tkinter.messagebox.showinfo('Ajuda',
"""Para pesquisar amostras, pesquise a localidade, escolha os parametros (tipo de imovel, metragem, tipo de venda).
Logo após finalizar o robo disponibilizará o arquivo na pasta indicada.
Para ler o arquivo abra no excel como CSV UTF-8.
Devido ao modo que o programa funciona, sempre haverá linhas em branco de excesso, por favor remova pelo excel.

Feito por : Nakamura""")


	def choose_directory(self):

		while True:
			try:
				file = filedialog.asksaveasfile(defaultextension=".csv",filetypes=(("Arquivo CSV", "*.csv"),("All Files", "*.*")))
				if not file:
					break
				else:
					if '.csv' not in file.name:
						raise ValueError
					self.directory = file.name
					break

			except ValueError:
				tkinter.messagebox.showinfo('Error', 'Formato de arquivo não suportado, salve apenas como .csv')


	


	def search(self,args):

		user_agent = get_random_ua()
		headers = {'user-agent': user_agent, }
		url ="https://glue-api.vivareal.com/v1/locations?q={0}&fields=suggest".format(args)

		

		try:
			print("Usando o IP da Jive")
			r = requests.get(url, headers = headers)
			print("Conseguiu com o IP da Jive")
		except Exception as e:
			print("Não conseguiu com o IP da jive, tentando os proxies")
			PROXY = module.get_free_proxies_2()
			# PROXY = 'http://'+PROXY

			http_proxy  = "http://"+PROXY
			https_proxy = "https://"+PROXY
			ftp_proxy   = "ftp://"+PROXY

			# print(PROXY)
			proxyDict = { 
					"http"  : http_proxy, 
					"https" : https_proxy, 
					"ftp"   : ftp_proxy
					}
			r = requests.get(url, headers = headers, proxies = proxyDict)


		if r.status_code == 200:

			data = json.loads(r.text)

			try:
				if self.queue: pass
			except AttributeError:
				self.create_queue_table()

			cities = []
			city = data.get("city")
			if city:
				result = city.get("result")
				locations = result.get("locations")
				for location in locations:

					address = location.get("address")
					locationId = address.get("locationId")
					estado = address.get("state")
					cidade = address.get("city")

					cities.append("{0} - {1}¨¨{2}".format(cidade,estado, locationId))

			neighborhoods = []
			neighborhood = data.get("neighborhood")
			if neighborhood:
				result = neighborhood.get("result")
				locations = result.get("locations")
				for location in locations:

					address = location.get("address")
					locationId = address.get("locationId")
					estado = address.get("state")
					cidade = address.get("city")
					bairro = address.get("neighborhood")

					neighborhoods.append("{0}, {1} - {2}¨¨{3}".format(bairro,cidade,estado, locationId))

			streets = []
			street = data.get("street")
			if street:
				result = street.get("result")
				locations = result.get("locations")
				for location in locations:

					address = location.get("address")
					locationId = address.get("locationId")
					estado = address.get("state")
					cidade = address.get("city")
					bairro = address.get("neighborhood")
					rua = address.get("street")

					streets.append("{0}, {1}, {2} - {3}¨¨{4}".format(rua,bairro,cidade,estado, locationId))

			self.create_city_table(cities,neighborhoods,streets)

		else:
			try:
				self.table.destroy()
				self.table_scrollbar.destroy()
			except AttributeError:
				pass
			self.nothing()


	def nothing(self):

		self.table = Listbox(self.root,width=40,height=5)
		self.table.insert('end', "Nada localizado")
		self.table.grid(row=6,column=0)

		self.title_3.grid(row=5,column=0)

	def value_appender(self,value):

		widget = value.widget
		selection=widget.curselection()
		value = widget.get(selection[0])

		self.popup(value)

	def popup(self,value):

		self.win = Toplevel()
		#win.wm_title("Window")

		Label(self.win, text="Área min.").grid(row=0, column=0)
		minima = Entry(self.win, width=4)
		minima.grid(row=0, column=1)

		Label(self.win, text="Área max.").grid(row=1, column=0)
		maxima = Entry(self.win, width=4)
		maxima.grid(row=1, column=1)

		lst1 = ['APARTAMENTO','CASA','CHÁCARA','CASA DE CONDOMINIO','FLAT','LOTE/TERRENO', 'LOTE/TERRENO (COMERCIAL)','SOBRADO','COBERTURA','KITNET','CONSULTORIO','EDIFICIO RESIDENCIAL','SALA COMERCIAL','FAZENDA/SITIO','GALPÃO/DEPÓSITO/ARMAZEM','IMOVEL COMERCIAL','LOJA','PONTO COMERCIAL']
		imovel = StringVar()
		drop = OptionMenu(self.win,imovel,*lst1)
		drop.grid(row=2, column=1)

		lst2 = ['VENDA','ALUGUEL']
		negocio = StringVar()
		drop_2 = OptionMenu(self.win,negocio,*lst2)
		drop_2.grid(row=3, column=1)

		Button(self.win, text="Ok", command=lambda: self.parse(minima,maxima,imovel,negocio,value)).grid(row=3, column=0)

	def parse(self,minima,maxima,imovel,negocio,value):

		var = {}
		var['locationId'] = value.split("¨¨")[1].strip()
		var['imovel'] = imovel.get()
		var['negocio'] = negocio.get()
		var['minima'] = minima.get()
		var['maxima'] = maxima.get()

		if (not var['imovel'] or not var['negocio']):

			tkinter.messagebox.showinfo('Error', 'Preencher os parametros para não causar erro')
			return

		self.queue.insert('end',var)
		self.win.destroy()

	def create_queue_table(self):

		self.queue = Listbox(self.root,width=160)
		self.queue.grid(row=6,column=1)
		scrollbar = Scrollbar(self.root, orient='vertical')
		scrollbar.config(command=self.queue.yview)
		scrollbar.grid(row=6,column=1,rowspan=2,sticky=N+S+E)

	def create_city_table(self,cities,neighborhoods,streets):

		self.title_3 = Label(self.root, text ='Resultado')

		self.table = Listbox(self.root,width=80,height=20)
		self.table.bind('<Double-Button-1>', self.value_appender)

		self.table_scrollbar = Scrollbar(self.root, orient='vertical')
		self.table_scrollbar.config(command=self.table.yview)

		if cities:
			self.table.insert("end", "Cidades")
			for c in cities:
				self.table.insert("end", c)

		if neighborhoods:
			self.table.insert("end", "Bairros")
			for n in neighborhoods:
				self.table.insert("end", n)

		if streets:
			self.table.insert("end", "Ruas")
			for z in streets:
				self.table.insert("end", z)

		for i,item in enumerate(self.table.get(0,END)):
			if item == 'Cidades':
				self.table.itemconfig(i, bg='gray')
			if item == 'Bairros':
				self.table.itemconfig(i, bg='gray')
			if item == 'Ruas':
				self.table.itemconfig(i, bg='gray')

		self.table.grid(row=6,column=0)
		self.table_scrollbar.grid(row=6,column=0,rowspan=5,sticky=N+S+E)
		self.title_3.grid(row=5,column=0)

	def run(self):

		from twisted.internet import reactor
		from scrapy.crawler import CrawlerProcess
		from scrapy.utils.log import configure_logging
		from vivareal.vivareal.spiders.vivareal import vivarealSpider

		try:
			len(self.directory)
		except AttributeError:
			tkinter.messagebox.showinfo('Error', 'Selecione um diretório para salvar as amostras')
			return

		try:
			if not (self.queue.get(0,END)):
				tkinter.messagebox.showinfo('Error', 'Lista de pesquisa vazia')
				return
		except AttributeError:
			tkinter.messagebox.showinfo('Error', 'Lista de pesquisa vazia')
			return

		params = []
		for i in self.queue.get(0,END):
			params.append(i)

		self.button_rodar.config(text='RODANDO',bg='red')
		self.root.update()

		time.sleep(1)

		configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
		process = CrawlerProcess({
			'FEED_FORMAT': 'csv',
			'FEED_URI': "file:///" + self.directory
		})
		process.crawl(vivarealSpider, (self.directory),(params))
		process.start()

		self.button_rodar.config(bg='darkgreen',state='disabled',text='FINALIZADO')

		### pegar o arquivo e deixar com o output amigável, salvar como excel
		# print(self.directory)  C:/Users/fabio.ruicci/Desktop/aaa.csv
		vr = pd.read_csv(self.directory)
		vr.drop_duplicates(inplace=True)

		vr.href = "www.vivareal.com.br" + vr.href
		vr.streetNumber = vr.streetNumber.apply(lambda x: streetnum(x))
		vr.street = vr.street.apply(lambda x: street2(x))
		vr["endereco"] = vr.street + ", " + vr.streetNumber

		vr.usableAreas = vr.usableAreas.apply(lambda x: tira_c(x))
		vr.bathrooms = vr.bathrooms.apply(lambda x: tira_c(x))
		vr.bedrooms = vr.bedrooms.apply(lambda x: tira_c(x))
		vr.parkingSpaces = vr.parkingSpaces.apply(lambda x: tira_c(x))

		vr["DT_LOAD"] = str(datetime.datetime.today().day)+"/"+str(datetime.datetime.today().month)+"/"+str(datetime.datetime.today().year)
		vr["DT_REF"] = str(datetime.datetime.today().day)+"/"+str(datetime.datetime.today().month)+"/"+str(datetime.datetime.today().year)

		# args
		df4 = vr[["businessType", "_id", "href", "title", "unitTypes", "description", "state", "city", "neighborhood", "endereco", "zipCode", "usableAreas", "bedrooms", "bathrooms", "parkingSpaces", "sale_price", "rental_price", "yearlyIptu", "monthlyCondoFee", "phones", "amenities", "DT_LOAD", "DT_REF"]].copy()
		### tirei "images",

		df4.columns = ["REFERENCIA", "ID", "LINK", "TITULO", "TIPO_IMOVEL", "DESCRICAO",
					   "UF", "CIDADE", "BAIRRO", "ENDERECO", "CEP", "AREA",
					   "QUARTOS", "BANHEIROS", "VAGAS", "VALOR_OFERTA", "ALUGUEL",
					   "IPTU", "CONDOMINIO", "TELEFONE", "CARACTERISTICAS", "DT_LOAD", "DT_REF"]
		### tirei "IMAGENS",

		df4.AREA = df4.AREA.apply(lambda x: numerico(x))
		df4.QUARTOS = df4.QUARTOS.apply(lambda x: numerico(x))
		df4.BANHEIROS = df4.BANHEIROS.apply(lambda x: numerico(x))
		df4.VAGAS = df4.VAGAS.apply(lambda x: numerico(x))
		df4.VALOR_OFERTA = df4.VALOR_OFERTA.apply(lambda x: numerico(x))
		df4.ALUGUEL = df4.ALUGUEL.apply(lambda x: numerico(x))
		df4 = df4[df4.AREA > 0]
		df4 = df4[(df4.VALOR_OFERTA > 0) | (df4.ALUGUEL > 0)]
		df4.REFERENCIA = df4.REFERENCIA.apply(lambda x: traduzir(x))
		df4.TIPO_IMOVEL = df4.TIPO_IMOVEL.apply(lambda x: traduzir(x))
		df4 = df4[df4.TIPO_IMOVEL != 'TIPO_IMOVEL']
		
		df4.to_excel(self.directory[:-3] + "xlsx", index = False)

		print("Finalizado")


if __name__ == "__main__":

	menu = Menu()
	menu.root.mainloop()
