from odoo import api, fields, models


class IcaMoneyExchange(models.Model):
    _name = "ica.money.exchange"
    _description = "Ica Money Exchange"

    name = fields.Char(string="Name")
    partner_id = fields.Many2one('res.partner', string="Customer")
    image_1920 = fields.Binary(string="Image", related='partner_id.image_1920')
    currency_id = fields.Many2one('res.currency', string="Currency",default=lambda  self:self.env.company.currency_id)
    line_ids = fields.One2many('ica.money.exchange.line', 'money_exchange_id')
    state = fields.Selection([('draft', 'Draft'),
                              ('in_progress', 'In Progress'),
                              ('done', 'Done'),
                              ('canceled', 'Canceled')], default='draft')

    def action_draft(self):
        self.state = 'draft'

    def action_in_progress(self):
        self.state = 'in_progress'

    def action_done(self):
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'


class IcaMoneyExchangeLine(models.Model):
    _name = "ica.money.exchange.line"
    _description = "Ica Money Exchange Line"

    money_exchange_id = fields.Many2one('ica.money.exchange')
    from_currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    from_amount = fields.Monetary(currency_field='from_currency_id')
    to_currency_id = fields.Many2one('res.currency',related="money_exchange_id.currency_id")
    to_amount = fields.Monetary(currency_field='to_currency_id')

    @api.onchange('from_currency_id', 'to_currency_id', 'from_amount')
    def _onchange_currency_id(self):
        if self.from_currency_id and self.to_currency_id and self.from_amount:
            self.to_amount = self.to_currency_id._convert(self.from_amount,self.from_currency_id)
