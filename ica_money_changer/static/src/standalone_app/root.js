/** @odoo-module */
import { Component } from "@odoo/owl";

export class Root extends Component {
    static template = "ica_money_changer.Root";
    static props = {};

    setup(){
        console.log("Heloi")
        this.todos = [
            {id:1,name:"HZN"},
            {id:2,name:"HZN"},
            {id:3,name:"HZN"},
            {id:4,name:"HZN"},
        ]
    }
}
