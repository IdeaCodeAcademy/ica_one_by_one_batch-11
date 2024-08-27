from odoo import api, fields, models


class CreateOrderWizard(models.TransientModel):
    _name = 'create.order.wizard'
    _description = 'CreateOrderWizard'

    partner_id = fields.Many2one('res.partner', string="Customer")
    currency_id = fields.Many2one('res.currency', string="Currency", default=lambda self: self.env.company.currency_id)
    date = fields.Date(string="Date", default=lambda self: fields.Date.today())
    line_ids = fields.One2many('create.order.wizard.line', 'order_id')

    def action_create_ica_order(self):
        context = self.env.context
        if context.get('active_model') == 'ica.money.exchange':
            ica_order = self.env['ica.order'].create({
                "partner_id": self.partner_id.id,
                "currency_id": self.currency_id.id,
                "money_exchange_id": context.get('active_id'),
                "line_ids": [
                    (0, 0, {"from_currency_id": line.from_currency_id.id, 'from_amount': line.from_amount})
                    for line in self.line_ids
                ]
            })
            ica_order.line_ids.mapped(lambda x: x._onchange_currency_id())
        # return {
        #     "type": "ir.actions.act_window",
        #     "res_model": "ica.order",
        #     "view_mode": "form",
        #     "target": "new",
        #     "res_id": ica_order.id
        # }


class CreateOrderWizardLine(models.TransientModel):
    _name = 'create.order.wizard.line'
    _description = 'CreateOrderWizardLine'

    order_id = fields.Many2one('create.order.wizard')
    from_currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    from_amount = fields.Monetary(currency_field='from_currency_id')
    to_currency_id = fields.Many2one('res.currency', related="order_id.currency_id")
    to_amount = fields.Monetary(currency_field='to_currency_id')

    @api.onchange('from_currency_id', 'to_currency_id', 'from_amount')
    def _onchange_currency_id(self):
        if self.from_currency_id and self.to_currency_id and self.from_amount:
            # self.to_amount = self.to_currency_id._convert(self.from_amount,self.from_currency_id)
            self.to_amount = self.from_currency_id._convert(self.from_amount, self.to_currency_id)
