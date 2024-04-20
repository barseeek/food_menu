function loadJSON(elementId){
    let element = document.getElementById(elementId);
    if (!element){
      log.error(`Not found element with id '${elementId}'.`)
      return null;
    }

    return JSON.parse(element.textContent);
}

let order_data = loadJSON('order_data');

Vue.createApp({
    name: "App",
    data(){
        return {
            data: order_data,
            selected_date: 0,
            quantity: 1,
            menu_prices: order_data.menu.map(item => (item.price)),
            allergies_prices: order_data.allergies.map(item => (item.price)),
        }
    },
    methods: {
        get_index(event) {
            return event.target.name.match(/\d+/g)[0];
        },
        select_date(event) {
            this.selected_date = event.target.value;
        },
        select_menu(event) {
            index = this.get_index(event);
            this.menu_prices[index] = (event.target.value == 0) ? this.data.menu[index].price : 0;
        },
        select_allergy(event) {
            index = this.get_index(event);
            this.allergies_prices[index] = (event.target.checked) ? 0: this.data.allergies[index].price;
        },
        select_quantity(event) {
            this.quantity = event.target.value;
        },
    },
    computed: {
        Cost() {
            return this.quantity * (this.data.date[this.selected_date].price +
                this.menu_prices.reduce((pre,curr)=>pre+curr,0) +
                this.allergies_prices.reduce((pre,curr)=>pre+curr,0))
        },
    }
}).mount('#VueApp')
