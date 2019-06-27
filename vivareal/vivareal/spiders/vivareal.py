import scrapy,yaml,json
from vivareal.vivareal.items import Anuncio

class vivarealSpider(scrapy.Spider):

	name = "vivareal"
	allowed_domains = ["glue-api.vivareal.com"]
	DOWNLOAD_DELAY = 0.50

	def __init__ (self, directory='',params='',*args):

		super(vivarealSpider,self).__init__(*args)

		self.directory = directory
		self.params = params

	def start_requests(self):

			for p in self.params:

				var = yaml.load(p)

				locationId = var["locationId"]
				minima = var["minima"]
				maxima = var["maxima"]

				businessType = var["negocio"]

				if businessType == "VENDA":
					businessType = "SALE"

				if businessType == "ALUGUEL":
					businessType = "RENTAL"

				unitType = var["imovel"]

				if unitType == "APARTAMENTO":
					unitType = "APARTMENT"

				if unitType == "CASA":
					unitType = "HOME"

				if unitType == "CASA DE CONDOMINIO":
					unitType = "CONDOMINIUM"

				if unitType == "CHÁCARA":
					unitType = "COUNTRY_HOUSE"

				if unitType == "COBERTURA":
					unitType = "PENTHOUSE"

				if unitType == "LOTE/TERRENO":
					unitType = "RESIDENTIAL_ALLOTMENT_LAND"

				if unitType == "SOBRADO":
					unitType = "TWO_STORY_HOUSE"

				if unitType == "CONSULTORIO":
					unitType = "CLINIC"

				if unitType == "RESIDENTIAL_BUILDING":
					unitType = "EDIFICIO RESIDENCIAL"

				if unitType == "FAZENDA/SITIO":
					unitType = "FARM"

				if unitType == "GALPÃO/DEPÓSITO/ARMAZEM":
					unitType = "SHED_DEPOSIT_WAREHOUSE"

				if unitType == "IMOVEL COMERCIAL":
					unitType = "COMMERCIAL_PROPERTY"

				if unitType == "LOJA":
					unitType = "STORE"

				if unitType == "LOTE/TERRENO (COMERCIAL)":
					unitType = "COMMERCIAL_ALLOTMENT_LAND"

				if unitType == "PONTO COMERCIAL":
					unitType = "BUSINESS"

				if unitType == "SALA COMERCIAL":
					unitType = "OFFICE"

				url = 'https://glue-api.vivareal.com/v1/listings?filter=((address.locationId LIKE "{0}%3E%25" OR address.locationId:"{0}")) '.format(locationId)

				if minima:
					url = url + "AND usableAreas >= {0}".format(minima)

				if maxima:
					url = url + "AND usableAreas <= {0}".format(maxima)

				url =  url + ' AND pricingInfos.businessType:"{0}" AND unitTypes:"{1}"&includeFields=addresses%2ClistingsLocation%2Cseo%2Csearch%2Curl%2Cexpansion%2Cfacets%2Cdevelopments&size=36&from=0'.format(businessType, unitType)

				yield scrapy.Request(url)


	def parse(self, response):

		data = json.loads(response.body)
		result = data["search"]["result"]
		listings = result['listings']

		if listings:

			for i in listings:

				item = Anuncio()

				listing = i["listing"]

				item["_id"]  = listing.get("id")
				item["amenities"] = listing.get("amenities")
				item["feedsId"]  = listing.get("feedsId")
				item["usableAreas"] = listing.get("usableAreas")
				item["description"] = listing.get("description")
				item["listingType"] = listing.get("listingType")
				item["videos"] = listing.get("videos")
				item["title"] = listing.get("title")
				item["createdAt"] = listing.get("createdAt")
				item["publisherId"] = listing.get("publisherId")
				item["unitTypes"] = listing.get("unitTypes")
				item["providerId"] = listing.get("providerId")
				item["condominiumName"] = listing.get("condominiumName")
				item["propertyType"] = listing.get("propertyType")
				item["suites"] = listing.get("suites")
				item["publicationType"] = listing.get("publicationType")
				item["externalId"] = listing.get("externalId")
				item["bathrooms"] = listing.get("bathrooms")
				item["totalAreas"] = listing.get("totalAreas")
				item["logoUrl"] = listing.get("logoUrl")
				item["bedrooms"] = listing.get("bedrooms")
				item["promotions"] = listing.get("promotions")
				item["highlights"] = listing.get("highlights")

				pricingInfos = listing.get("pricingInfos")

				if pricingInfos :

					item["yearlyIptu"] = pricingInfos[0].get("yearlyIptu")
					item["monthlyCondoFee"] = pricingInfos[0].get("monthlyCondoFee")
					item["businessType"] = ','.join([x.get("businessType") for x in pricingInfos])

					for p in pricingInfos:

						if p.get("businessType") == "SALE":
							item["sale_price"] =  p.get("price")
						elif p.get("businessType") == "RENTAL":
							item["rental_price"] = p.get("price")


				item["showPrice"] = listing.get("showPrice")
				item["displayAddress"] = listing.get("displayAddress")

				contact = listing.get("contact")
				item["phones"] = contact.get("phones")

				item["listingStatus"] = listing.get("listingStatus")
				item["parkingSpaces"] = listing.get("parkingSpaces")
				item["updatedAt"] = listing.get("updatedAt")
				item["images"] = listing.get("images")

				address = listing.get("address")

				item["country"] = address.get("country")
				item["state"] = address.get("state")
				item["city"] = address.get("city")
				item["neighborhood"] = address.get("neighborhood")
				item["street"] = address.get("street")
				item["streetNumber"] = address.get("streetNumber")
				item["unitNumber"] = address.get("unitNumber")
				item["zipCode"] = address.get("zipCode")
				item["locationId"] = address.get("locationId")
				item["zone"] = address.get("zone")
				item["district"] = address.get("district")

				geoLocation = address.get("geoLocation")
				if geoLocation:
					item["precision"] = geoLocation.get("precision")

					location = geoLocation.get("location")
					item["latitude"] = location.get("lat")
					item["longitude"] = location.get("lon")

				url = i["url"]
				link = url.get("link")
				item["href"] = link.get("href")

				item["properAddress"] = i["properAddress"]
				publisherUrl = i["publisherUrl"]
				link = publisherUrl.get("link")
				item["publisherUrl"] = link.get("href")

				yield item

			url = response.url.split('&from=')

			next_page = int(url[1]) + 36

			url = url[0] + "&from=" + str(next_page)

			yield scrapy.Request(url=url)
