# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from odoo.exceptions import Warning
import random
from datetime import date, datetime

class PosMultiShop(models.Model):
	_name = 'pos.multi.shop'
	_description = "POS Multi Shop"

	name = fields.Char('Name', required=True)
	config_id = fields.Many2one('pos.config', 'Point of Sale')
	stock_location_id = fields.Many2one('stock.location', 'Stock Location')
	picking_type_id = fields.Many2one('stock.picking.type', 'Stock Picking Type')
	related_partner_id = fields.Many2one('res.partner', 'Related Partner')
	street = fields.Char('Street')
	street2 = fields.Char('Street2')
	city = fields.Char('City')
	zip = fields.Char('Zip')
	state_id = fields.Many2one('res.country.state', 'State')
	country_id = fields.Many2one('res.country', 'Country')
	website = fields.Char('Website')
	phone = fields.Char('Phone')
	email = fields.Char('Email')
	product_ids = fields.Many2many('product.product', string='Products',
		domain = [('available_in_pos', '=', True)])
	image = fields.Binary('Image')
	
	
	@api.model
	def create(self, value):
		pos_shop = super(PosMultiShop, self).create(value)
		for shop in pos_shop.product_ids:
			shop.update({'shop_ids':[(4, pos_shop.id)], 'available_in_shop': 'specific'})
		return pos_shop

	def write(self,value):
		pos_shop = super(PosMultiShop, self).write(value)
		for shop in self.product_ids:
			shop.update({'shop_ids':[(4, self.id)], 'available_in_shop': 'specific'})
		return pos_shop
	
	
	@api.onchange('related_partner_id')
	def partner_info_update(self):
		if self.related_partner_id:
			self.update({
				'street': self.related_partner_id.street, 
				'street2': self.related_partner_id.street2, 
				'city': self.related_partner_id.city,
				'zip': self.related_partner_id.zip,
				'state_id': self.related_partner_id.state_id,
				'country_id': self.related_partner_id.country_id,
				'email': self.related_partner_id.email,
				'website': self.related_partner_id.website,
				'phone': self.related_partner_id.phone,
			})
	

class POSConfigShop(models.Model):
	_inherit = 'pos.config'
	
	shop_id = fields.Many2one('pos.multi.shop', 'Shop')

class POSSessionShop(models.Model):
	_inherit = 'pos.session'

	def get_shop_id(self):
		session = self.env['pos.session'].search([('state','=','opened'),('user_id','=',self.env.uid)])
		if session:
			return session.config_id.shop_id.id

	
class ProductPosShop(models.Model):
	_inherit = 'product.product'
	
	available_in_shop = fields.Selection([('all','All'),('specific','Specific')], default='all', string='Available in POS Shop')
	shop_ids = fields.Many2many('pos.multi.shop', string='POS Shop')
	
	def get_shop_product(self):
		shop_obj = self.env['pos.config'].search([])
		for sh in shop_obj.shop_id.product_ids:
			return sh
	

	
	

