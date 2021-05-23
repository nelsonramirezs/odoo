odoo.define('bi_pos_multi_shop.pos', function(require) {
	"use strict";

	var models = require('point_of_sale.models');

	models.load_fields('product.product', ['shop_ids']);

	models.load_models({
		model: 'pos.multi.shop',
		fields: ['name', 'config_id','stock_location_id','picking_type_id', 'related_partner_id', 'product_ids'],
		domain: [],
		loaded: function(self, pos_shops){
			 self.pos_shops = pos_shops;
		},
	});
 
});
