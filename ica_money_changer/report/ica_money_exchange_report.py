from odoo import models


class IcaMoneyExchangeReportXlsx(models.AbstractModel):
    _name = 'report.ica_money_changer.ica_money_exchange'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, ica_money_exchange_ids):
        x, y = 2, 0
        for obj in ica_money_exchange_ids:
            # One sheet by partner
            sheet = workbook.add_worksheet(obj.name)
            bold = workbook.add_format({'bold': True})
            sheet.write(0, 0, obj.name, bold)
            for ica_order_id in obj.ica_order_ids:
                sheet.write(x, y, ica_order_id.id, bold)
                sheet.write(x, y + 1, ica_order_id.name, bold)
                sheet.write(x, y + 2, ica_order_id.currency_id.name, bold)
                sheet.write(x, y + 3, ica_order_id.total_amount, bold)
                x += 1
            sheet.write(x, y+2, 'Total', bold)
            abc = ['A','B','C','D']
            # sheet.write(x, y+3, sum(obj.ica_order_ids.mapped('total_amount')), bold)
            # sheet.write(x, y+3,f'=SUM(D1:D5)', bold)
            sheet.write(x, y+3,f'=SUM({abc[y+3]}3:{abc[y+3]}{x})')
