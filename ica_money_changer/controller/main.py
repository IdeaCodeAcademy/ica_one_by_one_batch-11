from odoo.http import Controller, route, request


class MainController(Controller):
    # @route([
    #     '/ica/home',
    #     '/ica/exchange-details/<model("ica.money.exchange"):exchange_id>'
    # ], type="http", auth="user", website=True, cors="*", csrf=False)
    # def index(self, exchange_id=None, **kw):
    #     # print(exchange_id)
    #     if exchange_id:
    #         return request.render('ica_money_changer.exchange_details', {"exchange_id": exchange_id})
    #     money_exchange_ids = request.env['ica.money.exchange'].search([])
    #     data = {
    #         "message": "Hello",
    #         "money_exchange_ids": money_exchange_ids,
    #     }
    #     return request.render('ica_money_changer.ica_home', data)
    #
    # @route('/ica/api/home', type="json", auth="user")
    # def ica_api_home(self, **kw):
    #     # print(kw)
    #     return {"message": "Welcome from Home."}
    #
    # @route('/ica/api/login', type="json", auth="none")
    # def ica_api_login(self, **kw):
    #     # print(kw)
    #     username = kw.get('username',None)
    #     password = kw.get('password',None)
    #     uid = request.session.authenticate(request.session.db,username, password)
    #     return {"message": "Login Successful.","uid":uid}

    @route("/ica_money_changer/standalone_app", auth="public")
    def standalone_app(self):
        return request.render(
            'ica_money_changer.standalone_app',
            {
                'session_info': request.env['ir.http'].get_frontend_session_info(),
            }
        )