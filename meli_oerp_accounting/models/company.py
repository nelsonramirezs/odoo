# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import fields, osv, models, api
from odoo.tools.translate import _
import logging
_logger = logging.getLogger(__name__)

import pdb
import requests

class ResCompany(models.Model):
    _name = "res.company"
    _inherit = "res.company"

    mercadolibre_process_payments_customer = fields.Boolean(string="Process payments from Customer")
    mercadolibre_process_payments_supplier_fea = fields.Boolean(string="Process payments fea to Supplier ML")
    mercadolibre_process_payments_supplier_shipment = fields.Boolean(string="Process payments shipping list cost to Supplier ML")

    mercadolibre_process_payments_journal = fields.Many2one("account.journal",string="Account Journal for MercadoLibre")
    mercadolibre_process_payments_res_partner = fields.Many2one("res.partner",string="MercadoLibre Partner")

    mercadolibre_order_confirmation = fields.Selection([ ("manual", "Manual"),
                                                ("paid_confirm", "Pagado>Confirmado"),
                                                ("paid_delivered", "Pagado>Entregado"),
                                                ("paid_confirm_with_invoice", "Pagado>Facturado"),
                                                ("paid_delivered_with_invoice", "Pagado>Facturado y Entregado")],
                                                string='Acción al recibir un pedido',
                                                help='Acción al confirmar una orden o pedido de venta')

    def hi(self):
        return True
