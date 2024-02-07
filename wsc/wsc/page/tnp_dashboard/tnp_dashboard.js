frappe.pages['tnp-dashboard'].on_page_load = function(wrapper) {
	new MyPage(wrapper)
}

MyPage = Class.extend({
	init: function(wrapper){
		this.page = frappe.ui.make_app_page({
			parent: wrapper,
			title: 'Training and Placement Dashboard',
			single_column: true
		});
		this.make()
	},
	make: function(){
		let all = $(this)
		$(frappe.render_template("tnp_dashboard" , {
			font_awesome_link:"https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css"
		})).appendTo(this.page.main)

		const container_list = document.querySelectorAll('.container')
		container_list[1].remove()

		cardData()
		chartData()
		tableData()
	}
})

const cardData = () =>{
	// card elements.
	let cardValue = document.querySelectorAll(".cardValue");

	// fetching values
	frappe.call({
		method: 'wsc.wsc.page.tnp_dashboard.tnp_dashboard.getCardData',
		callback: function(res){
			for(let i=0; i<cardValue.length; i++){
				cardValue[i].innerText = i;
			}
		}
	})
}

const chartData = () =>{

}
const tableData = () =>{

}