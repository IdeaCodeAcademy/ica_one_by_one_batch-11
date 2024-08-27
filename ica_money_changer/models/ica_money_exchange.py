from odoo import api, fields, models, _


class IcaMoneyExchange(models.Model):
    _name = "ica.money.exchange"
    _description = "Ica Money Exchange"
    _inherit = ['mail.thread','mail.activity.mixin']

    name = fields.Char(string="Name", default=lambda self: _("New"), readonly=True, copy=False)
    partner_id = fields.Many2one('res.partner', string="Customer")
    image_1920 = fields.Binary(string="Image", related='partner_id.image_1920')
    currency_id = fields.Many2one('res.currency', string="Currency", default=lambda self: self.env.company.currency_id)
    line_ids = fields.One2many('ica.money.exchange.line', 'money_exchange_id')
    state = fields.Selection([('draft', 'Draft'),
                              ('in_progress', 'In Progress'),
                              ('done', 'Done'),
                              ('canceled', 'Canceled')], default='draft',tracking=True)
    total_amount = fields.Monetary(compute="_compute_total_amount")
    ica_order_ids = fields.One2many('ica.order', 'money_exchange_id')
    ica_order_count = fields.Integer(compute="_compute_ica_order_count")

    def _compute_ica_order_count(self):
        for rec in self:
            rec.ica_order_count = len(rec.ica_order_ids)

    def action_ica_order(self):
        return {
            "name":f"{self.name}'s orders",
            "type": "ir.actions.act_window",
            "res_model": "ica.order",
            "domain": [('id', 'in', self.ica_order_ids.ids)],
            "view_mode": "tree"
        }

    @api.model
    def create(self, values):
        # Add code here
        if values.get('name', _("New")) == _("New"):
            values['name'] = self.env['ir.sequence'].next_by_code('ica.money.exchange') or _("New")
        return super(IcaMoneyExchange, self).create(values)

    @api.depends('line_ids.to_amount')
    def _compute_total_amount(self):
        if self.line_ids:
            self.total_amount = sum(self.line_ids.mapped('to_amount'))
        else:
            self.total_amount = 0.0

    def action_draft(self):
        self.state = 'draft'

    def action_in_progress(self):
        self.state = 'in_progress'

    def action_done(self):
        wizard = self.env['create.order.wizard'].create({
            "partner_id": self.partner_id.id,
            "currency_id": self.currency_id.id,
            "line_ids": [
                (0, 0, {"from_currency_id": line.from_currency_id.id, 'from_amount': line.from_amount})
                for line in self.line_ids
            ]
        })
        wizard.line_ids.mapped(lambda x: x._onchange_currency_id())
        return {
            "type": "ir.actions.act_window",
            "res_model": "create.order.wizard",
            "view_mode": "form",
            "target": "new",
            "res_id": wizard.id
        }
        # self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'


class IcaMoneyExchangeLine(models.Model):
    _name = "ica.money.exchange.line"
    _description = "Ica Money Exchange Line"

    money_exchange_id = fields.Many2one('ica.money.exchange')
    from_currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    from_amount = fields.Monetary(currency_field='from_currency_id')
    to_currency_id = fields.Many2one('res.currency', related="money_exchange_id.currency_id")
    to_amount = fields.Monetary(currency_field='to_currency_id')

    @api.onchange('from_currency_id', 'to_currency_id', 'from_amount')
    def _onchange_currency_id(self):
        if self.from_currency_id and self.to_currency_id and self.from_amount:
            # self.to_amount = self.to_currency_id._convert(self.from_amount,self.from_currency_id)
            self.to_amount = self.from_currency_id._convert(self.from_amount, self.to_currency_id)
