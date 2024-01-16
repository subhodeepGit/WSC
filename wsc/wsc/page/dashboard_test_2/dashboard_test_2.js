frappe.pages['dashboard-test-2'].on_page_load = function(wrapper) {
	new MyPage(wrapper)
}

const frappe_charts = document.querySelector("#frappe-charts")
//Page Content
MyPage = Class.extend({
	init: function(wrapper){
		this.page = frappe.ui.make_app_page({
			parent: wrapper,
			title: 'test',
			single_column: true
		});
		
		this.make()
	} , 
	// make page
	make : function(){
		//grab the class
		let all = $(this)
		//push dom element to page
		
		let data = function(){
			frappe.call({
				// apps/wsc/wsc/wsc/page/dashboard_test_2/dashboard_test_2.py
				method:'wsc.wsc.page.dashboard_test_2.dashboard_test_2.get_data',
				callback:function(r){
					// console.log(r.message);
					let labels = []
					let values = []
					let values_absent = []
					let values_present = []
					console.log(r.message[0]);

					//present & absent
					r.message.map((i) => {
				
						labels.push(`${i.date}-${i.course_schedule}`)
						values_present.push(i.PresentCount)
						values_absent.push(i.AbsentCount)
						
					})
					values = [values_present , values_absent]
					
					document.querySelector("#trainer-id").innerText = r.message[0].owner
					chart(labels , values)
				}
			})
		}
		//Unable to put up conflicting data like present and absent either it turns all dates present , no absent or none at all
		const chart = function(labels , values){
			const chart_data = {
				labels, //x-axis
				datasets:[
					{
						name: "Student Present", type: "bar",
						values:values[0]
					},
					{
						name: "Student Absent", type: "bar",
						values:values[1]
					}
				],
				yMarkers:[
					{
						label:"Student Present" ,
						value:10
					},
					// {
					// 	label:"Student Absent" ,
					// 	value:10
					// }
				],
				yRegions: [{
					label:"Attendance", start: 0 , end:10 , 
					options:{ labelPos:'left'}
				}]
			}
			
			const chart = new frappe.Chart("#frappe-charts", {  // or a DOM element,
														// new Chart() in case of ES6 module with above usage
				title: "Student Attendance Chart",
				data: chart_data,
				type: 'bar', // or 'bar', 'line', 'scatter', 'pie', 'percentage' , axis-mixed
				height: 250,
				colors: ['#7cd6fd', '#743ee2']
			})

			// chart.removeDataPoint(0,2)
		}

		
		$(frappe.render_template(frappe.dashboard_test_page.body , this)).appendTo(this.page.main)

		data()
		// chart()
		// $(frappe.render_template(body , this)).appendTo(this.page.main)
	}
})


{/* <script src="https://cdn.jsdelivr.net/npm/frappe-charts@1.6.1/dist/frappe-charts.min.umd.js"></script> */}
let body = `

<div class="widget-group ">
<div class="widget-group-head">
	
	<div class="widget-group-control"></div>
</div>
<div class="widget-group-body grid-col-3"><div class="widget number-widget-box" data-widget-name="Total Declaration Submitted">
<div class="widget-head">
<div class="widget-label">
	<div class="widget-title"><span class="ellipsis" title="Total Declaration Submitted" style="color:red">Owner</span></div>
	<div class="widget-subtitle"></div>
</div>
<div class="widget-control"><div class="card-actions dropdown pull-right">
<a data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
...
</a>
<ul class="dropdown-menu" style="max-height: 300px; overflow-y: auto;">
	<li class="dropdown-item">
					<a data-action="action-refresh">Refresh</a>
				</li><li class="dropdown-item">
					<a data-action="action-edit">Edit</a>
				</li>
</ul>
</div></div>
</div>
<div class="widget-body"><div class="widget-content">
<div class="number" style="color:undefined" id="trainer-id">0</div>
</div></div>
<div class="widget-footer"></div>
</div><div class="widget number-widget-box" data-widget-name="Total Salary Structure">
<div class="widget-head">
<div class="widget-label">
	<div class="widget-title"><span class="ellipsis" title="Total Salary Structure" >Total Salary Structure</span></div>
	<div class="widget-subtitle"></div>
</div>
<div class="widget-control"><div class="card-actions dropdown pull-right">
<a data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
...
</a>
<ul class="dropdown-menu" style="max-height: 300px; overflow-y: auto;">
	<li class="dropdown-item">
					<a data-action="action-refresh">Refresh</a>
				</li><li class="dropdown-item">
					<a data-action="action-edit">Edit</a>
				</li>
</ul>
</div></div>
</div>
<div class="widget-body"><div class="widget-content">
<div class="number" style="color:undefined">1</div>
<div class="card-stats grey-stat">
<span class="percentage-stat-area">
	
	<span class="percentage-stat">
		0  %
	</span>
</span>
<span class="stat-period text-muted">
	since last month
</span>
</div></div></div>
<div class="widget-footer"></div>
</div><div class="widget number-widget-box" data-widget-name="Total Incentive Given(Last month)">
<div class="widget-head">
<div class="widget-label">
	<div class="widget-title"><span class="ellipsis" title="Total Incentive Given(Last month)">Total Incentive Given(Last month)</span></div>
	<div class="widget-subtitle"></div>
</div>
<div class="widget-control"><div class="card-actions dropdown pull-right">
<a data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
...
</a>
<ul class="dropdown-menu" style="max-height: 300px; overflow-y: auto;">
	<li class="dropdown-item">
					<a data-action="action-refresh">Refresh</a>
				</li><li class="dropdown-item">
					<a data-action="action-edit">Edit</a>
				</li>
</ul>
</div></div>
</div>
<div class="widget-body"><div class="widget-content">
<div class="number" style="color:undefined">₹ 0.00 </div>
</div></div>
<div class="widget-footer"></div>
</div><div class="widget number-widget-box" data-widget-name="Total Outgoing Salary(Last month)">
<div class="widget-head">
<div class="widget-label">
	<div class="widget-title"><span class="ellipsis" title="Total Outgoing Salary(Last month)">Total Outgoing Salary(Last month)</span></div>
	<div class="widget-subtitle"></div>
</div>
<div class="widget-control"><div class="card-actions dropdown pull-right">
<a data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
...
</a>
<ul class="dropdown-menu" style="max-height: 300px; overflow-y: auto;">
	<li class="dropdown-item">
					<a data-action="action-refresh">Refresh</a>
				</li><li class="dropdown-item">
					<a data-action="action-edit">Edit</a>
				</li>
</ul>
</div></div>
</div>
<div class="widget-body"><div class="widget-content">
<div class="number" style="color:undefined">₹ 0.00 </div>
</div></div>
<div class="widget-footer"></div>
</div></div>
</div>
<div id="frappe-charts"></div>
`


// HTML content
frappe.dashboard_test_page = {
	body:body
}