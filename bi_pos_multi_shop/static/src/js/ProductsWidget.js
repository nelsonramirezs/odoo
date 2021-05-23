// BiProductScreen js
odoo.define('bi_pos_multi_shop.ProductsWidget', function(require) {
	"use strict";

	const PosComponent = require('point_of_sale.PosComponent');
	const Registries = require('point_of_sale.Registries');
	const { useListener } = require('web.custom_hooks');
	const { onChangeOrder, useBarcodeReader } = require('point_of_sale.custom_hooks');
	const { useState } = owl.hooks;

	const ProductsWidget = require('point_of_sale.ProductsWidget');

	const BiProductsWidget = (ProductsWidget) =>
		class extends ProductsWidget {
			constructor() {
				super(...arguments);
			}

			get productsToDisplay() {
				let self = this;
				let prods = super.productsToDisplay;
				let new_prods = [];
				let config_shop = self.env.pos.config.shop_id;
				if(config_shop){
					config_shop = config_shop[0];
					$.each(prods, function( i, prd ){
						if(prd.shop_ids){
							let is_valid = prd.shop_ids.indexOf(config_shop);
							if(is_valid >= 0){new_prods.push(prd);}
						}
					});
					return new_prods;
				}
				else{
					return prods;
				}
			}
		};

	Registries.Component.extend(ProductsWidget, BiProductsWidget);

	return ProductsWidget;

});
