{
    "name": "Money Changer",
    "author": "Han Zaw yein",
    "depends": ["base", "mail", "report_xlsx"],
    "license": "LGPL-3",
    "data": [
        "report/ica_money_exchange_excel_report.xml",
        "report/ica_money_exchange_report.xml",
        "data/sequence.xml",
        "security/ir.model.access.csv",
        "views/ica_money_exchange.xml",
        "views/ica_order.xml",
        "wizard/create_order_wizard.xml",
        "views/client_action.xml",

        "views/menus.xml",
    ],
    "assets": {
        "web.assets_backend": [
            # "ica_money_changer/static/src/client_action/**/*",
            "ica_money_changer/static/src/client_action/client_action.js",
            "ica_money_changer/static/src/client_action/client_action.xml",
        ]
    }
}
