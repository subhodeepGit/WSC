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
				cardValue[i].innerText = res.message[i];
			}
		}
	})
}

const chartData = () =>{
	// chart containers
	let chartContainer1 = document.getElementById('chartHolder1');
	let chartContainer2 = document.getElementById('chartHolder2');
	let chartContainer3 = document.getElementById('chartHolder3');
	let chartContainer4 = document.getElementById('chartHolder4');
	let chartContainer5 = document.getElementById('chartHolder5');
	let chartContainer6 = document.getElementById('chartHolder6');
	let chartContainer7 = document.getElementById('chartHolder7');
	let chartContainer8 = document.getElementById('chartHolder8');

  // Data for the donut chart
  var data = {
    labels: ["A", "B", "C", "D", "E"],
    datasets: [
      {
        values: [20, 30, 15, 25, 10]
      }
    ]
  };

  // Options for the donut chart without labels
  var donutOptions = {
    title: "",
    colors: ["#FF5733", "#FFBD33", "#33FF77", "#3366FF", "#FF33A1"],
    donutWidth: 20,
    height: (chartContainer1.clientHeight)
  };

  const options = {
    type: 'bar',
    colors: ['#7cd6fd'],
    axisOptions: {
        xAxisMode: 'tick',
        yAxisMode: 'span'
    },
    barOptions: {
        spaceRatio: 0.2
    },
	height: 150
};

  // Create a new Frappe Chart instance for donut chart without labels

//   chart 1
  var chart = new frappe.Chart("#chartHolder1", {
    title: donutOptions.title,
    data: data,
    type: 'donut',
    height: donutOptions.height,
    colors: donutOptions.colors,
    donutWidth: donutOptions.donutWidth,
  });
  //   chart 2
  var chart = new frappe.Chart("#chartHolder2", {
    title: options.title,
    data: data,
    type: 'bar',
    height: options.height,
    colors: options.colors,
  });
//   chart 3
  var chart = new frappe.Chart("#chartHolder3", {
    title: options.title,
    data: data,
    type: 'bar',
    height: options.height,
    colors: options.colors,
  });
  //   chart 4
  var chart = new frappe.Chart("#chartHolder4", {
    title: donutOptions.title,
    data: data,
    type: 'donut',
    height: donutOptions.height,
    colors: donutOptions.colors,
    donutWidth: donutOptions.donutWidth,
  });
  //   chart 5
  var chart = new frappe.Chart("#chartHolder5", {
    title: donutOptions.title,
    data: data,
    type: 'donut',
    height: donutOptions.height,
    colors: donutOptions.colors,
    donutWidth: donutOptions.donutWidth,
  });
  //   chart 6
  var chart = new frappe.Chart("#chartHolder6", {
    title: options.title,
    data: data,
    type: 'bar',
    height: options.height,
    colors: options.colors,
    donutWidth: options.donutWidth,
  });
//   chart 7
  var chart = new frappe.Chart("#chartHolder7", {
    title: options.title,
    data: data,
    type: 'bar',
    height: options.height,
    colors: options.colors,
    donutWidth: options.donutWidth,
  });
  //   chart 8
  var chart = new frappe.Chart("#chartHolder8", {
    title: donutOptions.title,
    data: data,
    type: 'donut',
    height: donutOptions.height,
    colors: donutOptions.colors,
    donutWidth: donutOptions.donutWidth,
  });
}
const tableData = () =>{
	let tableHolder = document.getElementById('driveTable');
	result = [
		{
			'val1': 'val1',
			'val2': 'val2',
			'val3': 'val3',
			'val4': 'val4',
			'val5': 'val5',
		},
		{
			'val1': 'val1',
			'val2': 'val2',
			'val3': 'val3',
			'val4': 'val4',
			'val5': 'val5',
		},
		{
			'val1': 'val1',
			'val2': 'val2',
			'val3': 'val3',
			'val4': 'val4',
			'val5': 'val5',
		},
		{
			'val1': 'val1',
			'val2': 'val2',
			'val3': 'val3',
			'val4': 'val4',
			'val5': 'val5',
		},
		{
			'val1': 'val1',
			'val2': 'val2',
			'val3': 'val3',
			'val4': 'val4',
			'val5': 'val5',
		},
		{
			'val1': 'val1',
			'val2': 'val2',
			'val3': 'val3',
			'val4': 'val4',
			'val5': 'val5',
		},
		{
			'val1': 'val1',
			'val2': 'val2',
			'val3': 'val3',
			'val4': 'val4',
			'val5': 'val5',
		},
		{
			'val1': 'val1',
			'val2': 'val2',
			'val3': 'val3',
			'val4': 'val4',
			'val5': 'val5',
		},
		{
			'val1': 'val1',
			'val2': 'val2',
			'val3': 'val3',
			'val4': 'val4',
			'val5': 'val5',
		},
		{
			'val1': 'val1',
			'val2': 'val2',
			'val3': 'val3',
			'val4': 'val4',
			'val5': 'val5',
		},
		{
			'val1': 'val1',
			'val2': 'val2',
			'val3': 'val3',
			'val4': 'val4',
			'val5': 'val5',
		},
		{
			'val1': 'val1',
			'val2': 'val2',
			'val3': 'val3',
			'val4': 'val4',
			'val5': 'val5',
		},
		{
			'val1': 'val1',
			'val2': 'val2',
			'val3': 'val3',
			'val4': 'val4',
			'val5': 'val5',
		},
		{
			'val1': 'val1',
			'val2': 'val2',
			'val3': 'val3',
			'val4': 'val4',
			'val5': 'val5',
		},
		{
			'val1': 'val1',
			'val2': 'val2',
			'val3': 'val3',
			'val4': 'val4',
			'val5': 'val5',
		},
		{
			'val1': 'val1',
			'val2': 'val2',
			'val3': 'val3',
			'val4': 'val4',
			'val5': 'val5',
		},
		{
			'val1': 'val1',
			'val2': 'val2',
			'val3': 'val3',
			'val4': 'val4',
			'val5': 'val5',
		},
		{
			'val1': 'val1',
			'val2': 'val2',
			'val3': 'val3',
			'val4': 'val4',
			'val5': 'val5',
		},
		{
			'val1': 'val1',
			'val2': 'val2',
			'val3': 'val3',
			'val4': 'val4',
			'val5': 'val5',
		},
		{
			'val1': 'val1',
			'val2': 'val2',
			'val3': 'val3',
			'val4': 'val4',
			'val5': 'val5',
		},
		{
			'val1': 'val1',
			'val2': 'val2',
			'val3': 'val3',
			'val4': 'val4',
			'val5': 'val5',
		},
		{
			'val1': 'val1',
			'val2': 'val2',
			'val3': 'val3',
			'val4': 'val4',
			'val5': 'val5',
		},
		{
			'val1': 'val1',
			'val2': 'val2',
			'val3': 'val3',
			'val4': 'val4',
			'val5': 'val5',
		},
	];

	frappe.call({
		method: 'wsc.wsc.page.tnp_dashboard.tnp_dashboard.getCardData',
		callback: function(res){
			let headerArr = ['Col1', 'Col2', 'Col3', 'Col4', 'Col5'];
                let element = document.querySelector('table');
                element.remove();
                let table = document.createElement('table');
                table.className = 'table';
                let thead = document.createElement('thead');
                let tbody = document.createElement('tbody');
                let tr = document.createElement('tr');

                for(let i = 0; i < headerArr.length; i++){
                    let th = document.createElement('th');
                    th.innerText = headerArr[i];
                    tr.appendChild(th);
                }
                for(let x in result){
                    let row = tbody.insertRow(x);
                    let objectLength = Object.values(result[x]).length;
                    for(let i = 0; i < objectLength; i++){
                        let data = Object.values(result[x])[i];
                        if(data != null){
                            row.insertCell(i).innerText = data;
                        }
                        else{
                            row.insertCell(i).innerText = " ";
                        }
                    }
                }
                thead.append(tr);
                table.append(thead);
                table.append(tbody);
                tableHolder.append(table);
		}
	})
}