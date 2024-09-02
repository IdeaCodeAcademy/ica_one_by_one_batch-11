/** @odoo-module **/

import {registry} from "@web/core/registry";

import {Component, useState} from "@odoo/owl";

class MoneyChangerClientAction extends Component {
    setup() {
        this.state = useState({
            nextId: 4,
            exchangeData: [
                {id: 1, name: 'HZN'},
                {id: 2, name: 'GG'},
                {id: 3, name: 'aeg'},
                {id: 4, name: 'asef'},
            ]
        })
    }

    addData() {
        this.state.nextId++;
        this.state.exchangeData.push({id: this.nextId, name: `Hello ${this.state.nextId}`});
        console.log(this.state.exchangeData);
    }

    deleteData(exchangeDataId) {
        console.log(exchangeDataId)
        this.state.exchangeData.splice(exchangeDataId, 1);
    }
}

MoneyChangerClientAction.template = "ica_money_changer.MoneyChangerClientAction";

// remember the tag name we put in the first step
registry.category("actions").add("ica_money_changer.MoneyChangerClientAction", MoneyChangerClientAction);