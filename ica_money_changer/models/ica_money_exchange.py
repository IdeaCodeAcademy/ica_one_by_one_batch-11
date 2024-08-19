from odoo import api, fields, models


class IcaMoneyExchange(models.Model):
    _name = "ica.money.exchange"
    _description = "Ica Money Exchange"

    name = fields.Char(string="Name")
    partner_id = fields.Many2one('res.partner', string="Customer")
    line_ids = fields.One2many('ica.money.exchange.line', 'money_exchange_id')


class IcaMoneyExchangeLine(models.Model):
    _name = "ica.money.exchange.line"
    _description = "Ica Money Exchange Line"

    money_exchange_id = fields.Many2one('ica.money.exchange')
    from_currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    from_amount = fields.Monetary(currency_field='from_currency_id')
    to_currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    to_amount = fields.Monetary(currency_field='to_currency_id')


