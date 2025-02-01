from reportlab.rl_settings import strikeGap

from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    invoice_count = fields.Integer(string="Invoice Count", compute='compute_get_invoice_count')
    invoice_ids = fields.Many2many('account.move', string='Invoices', compute='_get_invoiced')
    invoiced_ids = fields.Many2many('account.move', string='Invoiced')

    @api.depends('invoice_ids')
    def compute_get_invoice_count(self):
        for record in self:
            count = 0
            for invoice in record.invoice_ids:
                if invoice:
                    count +=1
            record.invoice_count = count
            print(record.invoice_count)
        print(self.invoice_ids, 'sale order invoice id')

    def invoice_id_test(self):
        print(self.id, 'test invoice id')

    @api.depends('invoiced_ids')
    def _get_invoiced(self):
        # The invoice_ids are obtained thanks to the invoice lines of the SO
        # lines, and we also search for possible refunds created directly from
        # existing invoices. This is necessary since such a refund is not
        # directly linked to the SO.
        for order in self:
            invoices = order.invoiced_ids
            order.invoice_ids = invoices
            order.invoice_count = len(invoices)



