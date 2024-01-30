frappe.pages['dashboard-director'].on_page_load = function(wrapper) {
	
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		// title: 'Dashboard For Director',
		single_column: true
	});

	const container_list = document.querySelectorAll('.mycontainer')
	const scroll_adjustments = document.querySelectorAll('.scroller')
	container_list[1].remove()
	
	// console.log(container_list[1]);
	$(frappe.render_template("dashboard_director" , {
		goole_fonts_link_1:"https://fonts.googleapis.com",
		goole_fonts_link_2:"https://fonts.gstatic.com",
		goole_fonts_link_3:"https://fonts.googleapis.com/css2?family=Roboto:wght@100;400&display=swap",
		font_awesome_link:"https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css",
		boxicons_link:"https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css",
	})).appendTo(page.body)
	
	progress_bar()
	// console.log(page.main , page.body);
}

function progress_bar(){
	console.log("hello there");
	const bars = document.querySelectorAll('.progress-bar');
    const color_mark = document.querySelectorAll('.color-mark')
    const percent_value = document.querySelectorAll('.percent')

    const values = [0, 100, 50]; // Set your progress values here
    const colors = ['#43c3e0' , '#f7dc6f'  , '#8382de']
	// console.log(bars);
    values.forEach((value, index) => {
        bars[index].style.width = `${value}%`;
        bars[index].style.backgroundColor = colors[index]

        color_mark[index].style.backgroundColor = colors[index]

        percent_value[index].innerText = `${value}%`
        
    });
}
// frappe.pages['dashboard-director'].on_page_load = function(wrapper) {
// 	new MyPage(wrapper)
// }

// MyPage = Class.extend({
// 	init:function(wrapper){
// 		this.page = frappe.ui.make_app_page({
// 			parent: wrapper,
// 			title: 'test',
// 			single_column: true
// 		});
// 		this.make()
// 	},
// 	make:function(){
// 		console.log(this.page.body);
// 	}
// })