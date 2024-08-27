from odoo import api, fields, models,_


class IcaOrder(models.Model):
    _name = 'ica.order'
    _inherit = "ica.money.exchange"
    _description = 'IcaOrder'

    line_ids = fields.One2many('ica.order.line', 'order_id')
    money_exchange_id = fields.Many2one('ica.money.exchange')

    @api.model
    def create(self, values):
        # Add code here
        if values.get('name',_('New')) == _('New'):
            values['name'] = self.env['ir.sequence'].next_by_code('ica.order')
        return super(IcaOrder, self).create(values)


class IcaMoneyExchangeLine(models.Model):
    _name = "ica.order.line"
    _description = "ICA Order Line"
    _inherit = "ica.money.exchange.line"

    order_id = fields.Many2one('ica.order')
    to_currency_id = fields.Many2one('res.currency',related="order_id.currency_id")

