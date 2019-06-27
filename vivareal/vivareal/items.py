# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Anuncio(scrapy.Item):

	_id = scrapy.Field()
	amenities = scrapy.Field()
	feedsId = scrapy.Field()
	usableAreas = scrapy.Field()
	description = scrapy.Field()
	listingType = scrapy.Field()
	videos = scrapy.Field()
	title = scrapy.Field()
	createdAt = scrapy.Field()
	publisherId = scrapy.Field()
	unitTypes = scrapy.Field()
	providerId = scrapy.Field()
	condominiumName = scrapy.Field()
	propertyType = scrapy.Field()
	suites = scrapy.Field()
	publicationType = scrapy.Field()
	externalId = scrapy.Field()
	bathrooms = scrapy.Field()
	totalAreas = scrapy.Field()
	logoUrl = scrapy.Field()
	bedrooms = scrapy.Field()
	promotions = scrapy.Field()
	highlights = scrapy.Field()
	yearlyIptu = scrapy.Field()
	monthlyCondoFee = scrapy.Field()
	businessType = scrapy.Field()
	sale_price = scrapy.Field()
	rental_price = scrapy.Field()
	showPrice = scrapy.Field()
	displayAddress = scrapy.Field()
	phones = scrapy.Field()
	listingStatus = scrapy.Field()
	parkingSpaces = scrapy.Field()
	updatedAt = scrapy.Field()
	images = scrapy.Field()
	country = scrapy.Field()
	state = scrapy.Field()
	city = scrapy.Field()
	neighborhood = scrapy.Field()
	street = scrapy.Field()
	streetNumber = scrapy.Field()
	unitNumber = scrapy.Field()
	zipCode = scrapy.Field()
	locationId = scrapy.Field()
	zone = scrapy.Field()
	district = scrapy.Field()
	precision = scrapy.Field()
	latitude = scrapy.Field()
	longitude = scrapy.Field()
	href = scrapy.Field()
	properAddress = scrapy.Field()
	publisherUrl = scrapy.Field()
