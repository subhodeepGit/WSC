frappe.ready(function() {
	// alert("hello")
	// frappe.web_form.after_load = () =>{
		// alert("hey")
	// frappe.web_form.on('enable',(field,value)=>{
	// 	alert("hehehe")
	// 	frappe.msgprint('Invalid mobile number')
	// });
	// frappe.web_form.on('dob',(field,value)=>{
	// 	if(value){
	// 		dob=new Date(value);
	// 		var today = new Date();
	// 		var age = Math.floor((today-dob)/(365.25*24*60*60*1000));
	// 		frappe.web_form.set_value("age",[age])
	// 	}
	// });
	frappe.web_form.validate= () =>{
		email_id=frappe.web_form.get_value("email_id");
		var pattern= /^\w+([-+.'][^\s]\w+)*@\w+([-.]\w+)*\.\w+([-,]\w)*$/;
		if (!pattern.test(email_id) && email_id){
			frappe.msgprint("Enter a valid email address");
			return false;
		}
		mob=frappe.web_form.get_value("phone_number");
		if (mob && mob.length!=10){
			frappe.msgprint('Mobile Number Should be 10 Digit.')
			return false;
		}
		mobileNum=frappe.web_form.get_value("phone_number");
		var validateMobNum= /^\d*(?:\.\d{1,2})?$/;
		if (!validateMobNum.test(mobileNum) && mobileNum){
			frappe.msgprint('Mobile Number Should be a Number')
			return false;
		}
		aadhar=frappe.web_form.get_value("aadhar_card_number");
		if (aadhar && aadhar.length!=10){
			frappe.msgprint('Aadhar Number Should be 12 Digit.')
			return false;
		}
		aadharNum=frappe.web_form.get_value("aadhar_card_number");
		var validateAadharNum= /^\d*(?:\.\d{1,2})?$/;
		if (!validateAadharNum.test(aadharNum) && aadharNum){
			frappe.msgprint('Aadhar Number Should be a Number')
			return false;
		}
		return true;
	}
	// };	
})
// frappe.web_form.after_load=()=>{
	
// 	//Phone number
// 	frappe.web_form.on('mobile_number',(field,value)=>{

// 		if(!(CheckSpecialchar(value)==false && CheckAlphabets(value)==false && value.length==10)){
// 			frappe.throw(__('Invalid mobile number'))
// 		}
// 	});
	// frappe.web_form.on('amount', (field, value) =&gt; {
	//     if (value &lt; 1000) {
	//         frappe.msgprint('Value must be more than 1000');
	//         field.set_value(0);
	//     }
	// });
	// frappe.web_form.after_load = () {
	//     alert("ehllo")
	// }
	// frappe.web_form.validate = () =&gt; {
	//     // return false if not valid
	// }
	// frappe.web_form.validate=()=>{
	// 	// frappe.throw("ehllo")
	// 	frappe.throw(__('Invalid mobile number'))
	// 	// frappe.msgprint('Please fill all values carefully');
	// 	//Phone number
		
	// }
	
