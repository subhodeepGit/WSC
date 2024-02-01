const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']	

frappe.pages['dashboard-director'].on_page_load = function(wrapper) {
	new MyPage(wrapper)
}

MyPage = Class.extend({
	init: function(wrapper){
		this.page = frappe.ui.make_app_page({
			parent: wrapper,
			title: 'test',
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
	}
	
})

const data = () => {

	let labels = []
	
	// DOM Element vairable
	const inactive_emp_details = document.querySelectorAll(".emp-detail")
	const jon_applicant_table = document.querySelectorAll(".table-row")
	const head_count = document.querySelector('#head-count')

	frappe.call({
		method:'wsc.wsc.page.dashboard_director.dashboard_director.get_data',
		callback:function(res){
			
			const [present_data , absent_data , on_leave_data , half_day_data , wfh_data] = paddedArrays(...res.message)
			
			const leave_records  = res.message[5]

			const job_applicant_records = res.message[6]

			const employee_count = res.message[7]
			const inactive_emp_count = res.message[8]
			const suspended_emp_count = res.message[9]
			const left_emp_count = res.message[10]

			const total_emp_count = res.message[11]

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
			
			// Inactive Emp Section
			inactive_emp(leave_records , inactive_emp_details)

			applicantSummaryDetails(job_applicant_records , jon_applicant_table)

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
const inactive_emp = (data , element) => {
	
	data.forEach((i , index) => {
		
		const employee_name = document.createElement('h4')
		const reasons = document.createElement('p')
		const emp_dates = document.createElement('p')

		reasons.classList.add('reasons')
		emp_dates.classList.add('emp-dates')

		employee_name.innerText = i.employee_name
		reasons.innerText = i.leave_type
		emp_dates.innerText = i.to_date
		
		younglingSlayer(element[index])
		
		element[index].appendChild(employee_name)
		element[index].appendChild(reasons)
		element[index].appendChild(emp_dates)

	})

}

const applicantSummaryDetails = (data , element) => {
	
	data.forEach((i, index) => {
		
		const applicant_name = document.createElement('div')
		const email_id = document.createElement('div')
		const designation = document.createElement('div')
		const status = document.createElement('div')
		const application_year = document.createElement('div')

		applicant_name.setAttribute('data-label' , "Applicant Name")
		email_id.setAttribute('data-label' , "Email Address")
		designation.setAttribute('data-label' , "Designation")
		status.setAttribute('data-label' , "Status")
		application_year.setAttribute('data-label' , "Applicantion Year")

		applicant_name.innerText = i.applicant_name
		email_id.innerText = i.email_id
		designation.innerText = i.designation
		status.innerText = i.designation
		application_year.innerText = i.application_year

		younglingSlayer(element[index])

		element[index].appendChild(applicant_name)
		element[index].appendChild(email_id)
		element[index].appendChild(designation)
		element[index].appendChild(status)
		element[index].appendChild(application_year)
	})
}

const employeeCount = (data, element) => {
	element.innerText = data[0].employee_count
}


function progress_bar(...data){
	
	const total_emp_count = data[3][0].total_count

	const inactive_emp_percent = Math.round((data[0][0].count/total_emp_count) * 100 , 2)
	const suspended_emp_percent = Math.round((data[1][0].count/total_emp_count) * 100 , 2)
	const left_emp_percent = Math.round((data[2][0].count/total_emp_count) * 100 , 2)

	const bars = document.querySelectorAll('.progress-bar');
    const color_mark = document.querySelectorAll('.color-mark')
    const percent_value = document.querySelectorAll('.percent')

    let values = [inactive_emp_percent , suspended_emp_percent , left_emp_percent]; // Set your progress values here
    const colors = ['#43c3e0' , '#f7dc6f'  , '#f5b7b1' ] 
	// , ' #f5b7b1 ' '#8382de'
	
    values.forEach((value, index) => {
		
        bars[index].style.width = `${value}%`;
        bars[index].style.backgroundColor = colors[index]

        color_mark[index].style.backgroundColor = colors[index]

        percent_value[index].innerText = `${value}%`

		percent_value[index].nextElementSibling.innerText = data[index][0].status
		console.log(percent_value[index].nextElementSibling);
        
    });
}

const chart = function(labels , ...values){ //add spread operator to values
	
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
		}]
	}
	
	const chart = new frappe.Chart("#frappe-graph", {  // or a DOM element,
												// new Chart() in case of ES6 module with above usage
		title: "Employee Attendance",
		data: chart_data,
		type: 'bar', // or 'bar', 'line', 'scatter', 'pie', 'percentage' , axis-mixed
		height: 250,
		colors: ['#7cd6fd', '#743ee2']
	})
	// chart.removeDataPoint(0,2)
}



