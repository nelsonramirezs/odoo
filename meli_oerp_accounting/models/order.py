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
from odoo.addons.meli_oerp.models.versions import *
from odoo.addons.meli_oerp_accounting.models.versions import *


class SaleOrder(models.Model):

    _inherit = "sale.order"

    def action_invoice_create(self, grouped=False, final=False):

        _invoices = super(SaleOrder,self)._create_invoices(grouped,final)

        #Colombia pragmatic
        for order in self:
            _logger.info(order)
            for inv in _invoices:
                _logger.info(inv)
                Invoice = self.env[acc_inv_model].browse([inv])
                if "fecha_entrega" in Invoice._fields:
                    _logger.info(Invoice)
                    if not Invoice.fecha_entrega:
                        Invoice.fecha_entrega =  order.commitment_date or order.expected_date
                        _logger.info(Invoice.fecha_entrega)
        return _invoices

    def meli_create_invoice( self, meli=None, config=None):
        _logger.info("meli_oerp_accounting meli_create_invoice started.")

        so = self
        #solo ordenes confirmadas o terminadas
    # TODO check meli_status_brief: if (self.meli_status_brief and "delivered" in self.meli_status_brief
        if so.state in ['sale','done']:
            #cond = so.invoice_status not in ['invoiced','no','upselling']
            cond = True and abs(so.meli_paid_amount - so.amount_total)<0.1
            dones = False
            cancels = False
            drafts = False
            if cond:
                #if so.picking_ids:
                #    for spick in so.picking_ids:
                #        _logger.info(str(spick)+" state:"+str(spick.state))
                #        if spick.state in ['done']:
                #            dones = True
                #        elif spick.state in ['cancel']:
                #            cancels = True
                #        else:
                #            drafts = True
                #else:
                #    dones = False

                #if drafts:
                    #drafts then nothing is full done
                #    dones = False
                dones = True

                if dones:
                    _logger.info("Creating invoice...")
                    invoices = self.env[acc_inv_model].search([(invoice_origin,'=',so.name)])

                    if not invoices:
                        _logger.info("Creating invoices")
                        result = so.action_invoice_create()
                        _logger.info("result:"+str(result))
                        invoices = self.env[acc_inv_model].search([(invoice_origin,'=',so.name)])
                        _logger.info("Created invoices: "+str(invoices))

                    if invoices:
                        for inv in invoices:
                            #try:
                            if inv.state in ['draft']:
                                _logger.info("Validate invoice: "+str(inv.name))
                                inv.action_post()
                                _logger.info("Created invoices and validated!")

                            #if inv.state in ['open']:
                            #    _logger.info("Send to Producteca: "+str(inv.name))
                            #    inv.orders_post_invoice()

                            #except:
                                #inv.message_post()
                            #    error = {"error": "Invoice Error"}
                            #    result.append(error)
                            #    raise;
                else:
                    _logger.info("Creating invoices not processed, shipment not complete: dones:"+str(False)+" drafts: "+str(drafts)+" cancels:"+str(cancels))

        _logger.info("meli_oerp_accounting meli_create_invoice ended.")

    def confirm_ml( self, meli=None, config=None ):
        _logger.info("meli_oerp_accounting confirm_ml")
        company = (config and 'company_id' in config._fields and config.company_id) or self.env.user.company_id
        config = config or company
        try:
            super(SaleOrder, self).confirm_ml(meli=meli,config=config)
            if (self.meli_orders):
                #process payments
                for meli_order in self.meli_orders:
                    for payment in meli_order.payments:
                        try:
                            if config.mercadolibre_process_payments_customer and not payment.account_payment_id:
                                payment.create_payment()
                        except Exception as e:
                            _logger.info("Error creating customer payment")
                            _logger.info(e, exc_info=True)
                        try:
                            if config.mercadolibre_process_payments_supplier_fea and not payment.account_supplier_payment_id:
                                payment.create_supplier_payment()
                        except Exception as e:
                            _logger.info("Error creating supplier fee payment")
                            _logger.info(e, exc_info=True)
                        try:
                            if config.mercadolibre_process_payments_supplier_shipment and not payment.account_supplier_payment_shipment_id and (payment.order_id and payment.order_id.shipping_list_cost>0.0):
                                payment.create_supplier_payment_shipment()
                        except Exception as e:
                            _logger.info("Error creating supplier shipment payment")
                            _logger.info(e, exc_info=True)
        except Exception as e:
            _logger.info("Confirm Payment Exception")
            _logger.error(e, exc_info=True)
            pass
        _logger.info("meli_oerp_accounting confirm_ml registering payments ended.")

        if "_invoice" in config.mercadolibre_order_confirmation:
            self.meli_create_invoice( meli=meli, config=config )

        _logger.info("meli_oerp_accounting confirm_ml ended.")
