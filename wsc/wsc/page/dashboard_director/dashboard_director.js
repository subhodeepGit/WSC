const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']	
frappe.pages['dashboard-director'].on_page_load = function(wrapper) {
	new MyPage(wrapper)
}

MyPage = Class.extend({
	init: function(wrapper){
		this.page = frappe.ui.make_app_page({
			parent: wrapper,
			// title: 'Director Dashboard',
			single_column: true
		});
		
		this.make()
	} , 
	make: function(){
		let all = $(this)

		$(frappe.render_template("dashboard_director" , {
			goole_fonts_link_1:"https://fonts.googleapis.com",
			goole_fonts_link_2:"https://fonts.gstatic.com",
			goole_fonts_link_3:"https://fonts.googleapis.com/css2?family=Roboto:wght@100;400&display=swap",
			font_awesome_link:"https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css",
		})).appendTo(this.page.main)

		data()

		const container_list = document.querySelectorAll('.container')
		container_list[1].remove()

		const col_md_12 = document.querySelectorAll(".col-md-12")
		col_md_12.forEach(i => {
			i.style.padding = 0;
		})
	}
	
})

const data = () => {

	let labels = []
	
	// DOM Element vairable
	const empOnLeave = document.querySelector("#emp-on-leave")
	const employee_renewal_table = document.querySelector("#table")
	const head_count = document.querySelector('#head-count')
	const holidays = document.querySelector('#holiday-table')

	frappe.call({
		method:'wsc.wsc.page.dashboard_director.dashboard_director.get_data',
		callback:function(res){
			
			const [present_data , absent_data , on_leave_data , half_day_data , wfh_data] = paddedArrays(...res.message)
			
			const leave_records  = res.message[5]

			const employee_renewals = res.message[6]

			const employee_count = res.message[7]
			const inactive_emp_count = res.message[8]
			const suspended_emp_count = res.message[9]
			const left_emp_count = res.message[10]

			const total_emp_count = res.message[11]
			
			const holiday_list = res.message[12]

			// Chart Section
			month_name_addition(present_data)
			month_name_addition(absent_data)
			month_name_addition(on_leave_data)
			month_name_addition(half_day_data)
			month_name_addition(wfh_data)

			present_data.forEach((i)=> {
				if(i) labels.push(`${i.month_name} - ${i.year}`)
			})
			absent_data.forEach(i => {
				if(i) labels.push(`${i.month_name} - ${i.year}`)
			})
			on_leave_data.forEach(i => {
				if(i) labels.push(`${i.month_name} - ${i.year}`)
			})
			half_day_data.forEach(i => {
				if(i) labels.push(`${i.month_name} - ${i.year}`)
			})
			wfh_data.forEach(i => {
				if(i) labels.push(`${i.month_name} - ${i.year}`)
			})

			labels = Array.from(new Set(labels));

			chart(labels , present_data , absent_data , on_leave_data , half_day_data , wfh_data)
			
			
			emp_on_leave(leave_records , empOnLeave)
			
			holidayDetails(holiday_list , holidays)

			employeeRenewalDetails(employee_renewals , employee_renewal_table)

			employeeCount(employee_count , head_count)

			progress_bar(inactive_emp_count , suspended_emp_count , left_emp_count , total_emp_count)

		}	
	})
}

//Dom , keys and array arrangments
const younglingSlayer = (element) => {
	while(element.firstChild){
		element.removeChild(element.firstChild);
	}
}
function month_name_addition(data){
	return data.forEach(i => {
		if(i) i.month_name = months[i.month - 1]
	})
}

function paddedArrays(...arrays) {
    // Find the length of the longest array
    let maxLength = Math.max(...arrays.map(arr => arr.length));

    // Pad shorter arrays with null (you can change it to any other value if needed)
    let paddedArrays = arrays.map(arr => {
        let paddingLength = maxLength - arr.length;
		
        return arr.concat(Array(paddingLength).fill(null));
    });

    return paddedArrays;
}

function swapArrayPositions(labels, data) {
	labels.forEach((monthYear, index) => {

		let label_split = monthYear.split(' - ')
		
		data.forEach((i , index2) => {
			
        	if (i && i.month_name === label_split[0] && String(i.year) === label_split[1]) {
				
				let key = i.status.toLowerCase().replace(/\s/g, '_');
				
				data[index] = i[key]
        	}

			if(!i){
				data[index2] = 0
			}

    	});	
	});
	
	return data
}

// Data and DOM works
const emp_on_leave = (data , element) => {
	
	younglingSlayer(element)

	data.forEach((i) => {
		
		const emp_details = document.createElement('div')

		const emp_id = document.createElement('p') 
		const employee_name = document.createElement('p')
		const reasons = document.createElement('p')
		const from_date = document.createElement('p')
		const to_date = document.createElement('p')

		emp_details.classList.add('emp-detail')

		emp_id.classList.add('employee-id')
		employee_name.classList.add('employee-name')
		reasons.classList.add('reasons')
		from_date.classList.add('emp-dates')
		to_date.classList.add('emp-dates')

		emp_id.innerText = i.name
		employee_name.innerText = i.employee_name
		reasons.innerText = i.leave_type
		from_date.innerText = i.from_date
		to_date.innerText = i.to_date
		
		emp_details.appendChild(emp_id)
		emp_details.appendChild(employee_name)
		emp_details.appendChild(from_date)
		emp_details.appendChild(to_date)
		emp_details.appendChild(reasons)
		
		element.appendChild(emp_details)

	})

	// Routing Emp on leaves
	element.addEventListener('click' , (e) => {
			
		e.preventDefault();
		
		if(e.target.classList.contains('employee-id') || e.target.classList.contains('employee-name') || e.target.classList.contains('reasons') || e.target.classList.contains('emp-dates')) frappe.set_route("Form" , "Leave Application" , e.target.closest('.emp-detail').children[0].innerText)	
	})
	
}

const holidayDetails = (data , element) => {
	
	younglingSlayer(element)

	data.forEach(i => {
		const holiday_row = document.createElement('div')

		const holiday_name = document.createElement('p')
		const date = document.createElement('p')
		const weekly_off = document.createElement('p')

		holiday_row.classList.add('holiday-detail')

		holiday_name.classList.add("holiday")
		date.classList.add('date')
		weekly_off.classList.add('weekly-off')

		holiday_name.innerText = i.name
		date.innerText = i.holiday_date
		
		if(i.weekly_off === 1) {
			weekly_off.innerText = 'Yes'
		} else{
			i.weekly_off = 'No'
		}

		holiday_row.appendChild(holiday_name)
		holiday_row.appendChild(date)
		holiday_row.appendChild(weekly_off)

		element.appendChild(holiday_row)
	})

	// element.addEventListener('click' , (e) => {
			
	// 	e.preventDefault();
	// 	console.log(e.target);
	// 	console.log(e.target.closest('.emp-detail').children[0].innerText);
	// 	frappe.set_route("Form", "Holiday List", "Saturday 2024"); //Exceptions
	// 	// if(e.target.classList.contains('holiday') || e.target.classList.contains('date') || e.target.classList.contains('weekly-off')) frappe.set_route("Form" , "Holiday List" , e.target.closest('.emp-detail').children[0].innerText)	
	// })
}

const employeeRenewalDetails = (data , element) => {

	younglingSlayer(element)

	data.forEach((i) => {
		const table_row = document.createElement('li')

		const id = document.createElement('p')
		const employee_id = document.createElement('p')
		const employee_name = document.createElement('p')
		const employement_type = document.createElement('p')
		const designation = document.createElement('p')
		const date_of_joining = document.createElement('p')
		const ctc = document.createElement('p')

		table_row.classList.add('table-row')

		id.classList.add('ID')
		employee_id.classList.add("Employee-ID")
		employee_name.classList.add("Employee-Name")
		employement_type.classList.add("Employement-Type")
		designation.classList.add("Designation")
		date_of_joining.classList.add("Date-of-joining")
		ctc.classList.add("CTC")

		id.innerText = i.name
		employee_id.innerText = i.employee
		employee_name.innerText = i.employee_name
		employement_type.innerText = i.employment_type
		designation.innerText = i.designation
		date_of_joining.innerText = i.date_of_joining
		ctc.innerText = i.cost_to_company_ctc

		table_row.appendChild(id)
		table_row.appendChild(employee_id)
		table_row.appendChild(employee_name)
		table_row.appendChild(employement_type)
		table_row.appendChild(designation)
		table_row.appendChild(date_of_joining)
		table_row.appendChild(ctc)

		element.appendChild(table_row)
	})
	
	//Routing Employee Renewal Applicants
	element.addEventListener('click' , (e) => {
				
		e.preventDefault()
		
		if(e.target.classList.contains('ID') || e.target.classList.contains('Employee-ID') || e.target.classList.contains('Employee-Name') || e.target.classList.contains('Employement-Type') || e.target.classList.contains('Designation') || e.target.classList.contains('Date-of-joining') || e.target.classList.contains('CTC')) frappe.set_route("Form" , "Employee Renewal Form" , e.target.closest('.table-row').children[0].innerText)
		
	})
}

const employeeCount = (data, element) => {

	const total_emp_button = document.querySelector('#total-emp')
	console.log(data);
	element.innerHTML = `${data[0].employee_count} <span>Employees</span>`  // One exception of all

	// total_emp_button.addEventListener('click' , (e) => {
	// 	e.preventDefault()
	// 	frappe.set_route("List", "Employee" , {
	// 		status: data[0].status
	// 	});
	// })
}


function progress_bar(...data){

	const bars = document.querySelectorAll('.progress-bar');
    const color_mark = document.querySelectorAll('.color-mark')
    const percent_value = document.querySelectorAll('.percent')

	const total_emp_count = data[3][0].total_count

	console.log(bars);

	const inactive_emp_percent = Math.round((data[0][0].count/total_emp_count) * 100 , 2)
	const suspended_emp_percent = Math.round((data[1][0].count/total_emp_count) * 100 , 2)
	const left_emp_percent = Math.round((data[2][0].count/total_emp_count) * 100 , 2)

    let values = [inactive_emp_percent , suspended_emp_percent , left_emp_percent]; // Set your progress values here
    const colors = ['#43c3e0' , '#f7dc6f'  , '#f5b7b1' ] 
	// , '#f5b7b1' '#8382de'
	
    values.forEach((value, index) => {
		
        bars[index].style.width = `${value}%`;
        bars[index].style.backgroundColor = colors[index]

        color_mark[index].style.backgroundColor = colors[index]

        percent_value[index].innerText = `${value}%`

		percent_value[index].nextElementSibling.innerText = data[index][0].status
        
    });

	// Progress Bar Routing
	bars.forEach((i , index) => {
		i.addEventListener('click' , (e) => {
			e.preventDefault()
			frappe.set_route("List", "Employee" , {
                status: data[index][0].status
            });
		})
	})

}

//Charts
const chart = function(labels , ...values){ //add spread operator to values
	
	const attendance_button = document.querySelector('#attendance')
	attendance_button.addEventListener('click' , (e) => {
		e.preventDefault()
		frappe.set_route("List", "Attendance");
	})

	const chart_data = {
		labels, //x-axis
		datasets:[
			{
				name: "Present", type: "bar",
				values:swapArrayPositions(labels , values[0])
			},
			{
				name: "Absent", type: "bar",
				values:swapArrayPositions(labels , values[1])
			},
			{
				name: "On Leave", type: "bar",
				values:swapArrayPositions(labels , values[2])
			},
			{
				name: "Half Day", type: "bar",
				values:swapArrayPositions(labels , values[3])
			},
			{
				name: "Work From Home", type: "bar",
				values:swapArrayPositions(labels , values[4])
			},
		],
		yMarkers:[
			{
				label:"Employee Attendance" ,
				value:10
			},
		],
		yRegions: [{
			label:"Employee Attendance", start: 0 , end:10 , 
			options:{ labelPos:'left'}
		}],
		// style: {
		// 	// Set the background color
		// 	"background-color": "#fff"
		// }  Doesnt Work 
	}
	
	const chart = new frappe.Chart("#frappe-graph", {  // or a DOM element,
												// new Chart() in case of ES6 module with above usage
		title: "Employee Attendance",
		data: chart_data,
		type: 'bar', // or 'bar', 'line', 'scatter', 'pie', 'percentage' , axis-mixed
		height: 550,
		colors: ['#43c3e0', '#f7dc6f' , '#f5b7b1' , '#8382de']
	})

	// chart.parent.addEventListener('data-select', (e) => {
	// 	update_moon_data(e.index); // e contains index and value of current datapoint
	// });
}



