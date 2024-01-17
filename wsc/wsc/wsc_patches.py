import frappe

BENCH_PATH = frappe.utils.get_bench_path()

def execute():
    disable_cancel_link()
    add_line_for_po()
    comment_lines_job_applicant()
    comment_lines_list_view()
    add_line_JobApplicant_js()
    update_line_gridrow_js()
    comment_line_FormSidebar_html()
    addi_sal_ret_bon()

def execute_security_patches():
    # upload_malicious_pdf()
    cross_site_scripting()
    login_password_encryption()
    login_password_decryption()
    add_login_html_overrides()
    insecure_transmission_password()
    improper_error_handling_response()
    process_response_website_js_1()
    process_response_website_js_2()
    change_password_confirmation_1()
    change_password_confirmation_2()
    update_forgot_password()
    login_senetize_handle()
    edit_line_file_preview()


def comment_line_FormSidebar_html():        #  wsc.wsc.wsc_patches.comment_line_FormSidebar_html
    file_path = "{}/{}".format(BENCH_PATH,"apps/frappe/frappe/public/js/frappe/form/templates/form_sidebar.html")
    
    with open(file_path, 'r') as file:
        content = file.read()

    content = content.replace('''<p><a class="small text-muted" href="https://github.com/frappe/{{ frappe.boot.module_app[frappe.scrub(frm.meta.module)] }}/issues/new"''', '''<!-- <p><a class="small text-muted" href="https://github.com/frappe/{{ frappe.boot.module_app[frappe.scrub(frm.meta.module)] }}/issues/new" -->''')
    content = content.replace('''target="_blank">''', '''<!-- target="_blank"> -->''')
    content = content.replace('''{{ __("Click here to post bugs and suggestions") }}</a></p>''', '''<!-- {{ __("Click here to post bugs and suggestions") }}</a></p> -->''')

    with open(file_path) as f:
        if '''<!-- <p><a class="small text-muted" href="https://github.com/frappe/{{ frappe.boot.module_app[frappe.scrub(frm.meta.module)] }}/issues/new" -->''' in f.read():
            return

    with open(file_path, 'w') as file:
        file.write(content)
        print("frappe/frappe/public/js/frappe/form/templates/form_sidebar.html commented Line.")

def edit_line_file_preview():
	file_path = "{}/{}".format(BENCH_PATH,"apps/frappe/frappe/public/js/frappe/file_uploader/FilePreview.vue")

	with open(file_path, 'r') as file:
		content = file.read()

	content = content.replace('''<input type="checkbox" :checked="optimize" @change="$emit('toggle_optimize')">Optimize</label>''', '''<input type="checkbox" :checked="optimize" @change="$emit('toggle_optimize')">Optimize (Compress files to reduce size)</label>''')
	content = content.replace('''<input type="checkbox" :checked="file.private" @change="$emit('toggle_private')">Private</label>''', '''<input type="checkbox" :checked="file.private" @change="$emit('toggle_private')">Private (Save files in private mode)</label>''')

	with open(file_path) as f:
		if '''<input type="checkbox" :checked="optimize" @change="$emit('toggle_optimize')">Optimize (Compress files to reduce size)</label>''' in f.read():
			return

	with open(file_path, 'w') as file:
		file.write(content)
		print("frappe/frappe/public/js/frappe/file_uploader/FilePreview.vue updated File Preview checkbox descriptions.")

def disable_cancel_link():
    file_path = "{}/{}".format(BENCH_PATH,
                               "apps/frappe/frappe/model/delete_doc.py")
    
    with open(file_path, "r") as file:
        content = file.read()
    
    updated_content = content.replace('Submitted Record cannot be deleted. You must {2} Cancel {3} it first.', 'Submitted Record cannot be deleted. You must Cancel it first.')

    with open(file_path) as f:
        if 'Submitted Record cannot be deleted. You must Cancel it first.' in f.read():
            return
        
    with open(file_path, "w") as file:
        file.write(updated_content)
        print("frappe/frappe/model/delete_doc.py modified Cancel link")


def add_line_for_po():
    file_path = "{}/{}".format(BENCH_PATH,"apps/erpnext/erpnext/public/js/controllers/taxes_and_totals.js")
    with open(file_path, "r") as file:
        content = file.readlines()
    target_line1 = 'flt(me.frm.doc.discount_amount) - tax.total, precision("rounding_adjustment"));'
    new_line1 = """\t\t\t\titem.gst=current_tax_amount;\n"""
    with open(file_path) as f:
        if """item.gst=current_tax_amount;""" in f.read():
            return
    index = -1
    for i, line in enumerate(content):
        if target_line1 in line:
            index = i
            break
    if index != -1:
        content.insert(index + 3, new_line1)
    with open(file_path, "w") as file:
        file.writelines(content)
        print("lines added for taxes and total")

def comment_lines_job_applicant():
    file_path = "{}/{}".format(BENCH_PATH,
                               "apps/hrms/hrms/hr/doctype/job_applicant/job_applicant.py")
    
    lines_to_comment = [
        "def autoname(self):",
        "self.name = self.email_id",
        'if frappe.db.exists("Job Applicant", self.name):',
        'self.name = append_number_if_name_exists("Job Applicant", self.name)'
    ]

    modified_lines = []

    with open(file_path, "r") as file:
        lines = file.readlines()

    for line in lines:
        if line.strip() in lines_to_comment:
            modified_line = "#" + line
            modified_lines.append(modified_line)
        else:
            modified_lines.append(line)

    if modified_lines != lines:
        with open(file_path, "w") as file:
            file.writelines(modified_lines)
        print("Commented lines in hrms/hrms/hr/doctype/job_applicant/job_applicant.py")


def comment_lines_list_view():
    file_path = "{}/{}".format(BENCH_PATH,
                               "apps/frappe/frappe/public/js/frappe/list/list_view.js")
    lines_to_comment = [
        "actions_menu_items.push(bulk_assignment());",
        "actions_menu_items.push(bulk_assignment_rule());",
        "actions_menu_items.push(bulk_add_tags());"
    ]

    modified_lines = []

    with open(file_path, "r") as file:
        lines = file.readlines()

    for line in lines:
        if line.strip() in lines_to_comment:
            modified_line = "//" + line
            modified_lines.append(modified_line)
        else:
            modified_lines.append(line)

    if modified_lines != lines:
        with open(file_path, "w") as file:
            file.writelines(modified_lines)
        print("Commented lines in apps/frappe/frappe/public/js/frappe/list/list_view.js")


def add_line_JobApplicant_js():
    input_file_path = "{}/{}".format(BENCH_PATH,
                                "apps/hrms/hrms/hr/doctype/job_applicant/job_applicant.js")

    with open(input_file_path, 'r') as file:
        lines = file.readlines()

    target_line = '\t\t\t\t\t\t__("Interview Summary")\n'
    line_to_add = '\t\t\t\t$("div").remove(".form-dashboard-section.custom");\n'

    line_added = False

    for i, line in enumerate(lines):
        if target_line in line:           
            if line_to_add not in lines:
                insert_index = i + 3
                lines.insert(insert_index, line_to_add)
                line_added = True
            break 

    if line_added:
        with open(input_file_path, 'w') as file:
            file.writelines(lines)
        print("Line added in hrms/hrms/hr/doctype/job_applicant/job_applicant.js")


def update_line_gridrow_js():    #  bench execute wsc.wsc.wsc_patches.update_line_gridrow_js
    input_file_path = "{}/{}".format(BENCH_PATH,
                                "apps/frappe/frappe/public/js/frappe/form/grid_row.js")
    

    with open(input_file_path, 'r') as file:
        lines = file.readlines()

    target_line_1 = 'if (cint(event.target.value) === 0) {'
    target_line_2 = 'frappe.throw(__("Column width cannot be zero."));'
    target_line_3 = '<div class="hidden-xs edit-grid-row">${__("Edit")}</div>'

    for i, line in enumerate(lines):
        if target_line_1 in line:
            # Modify the first target line's condition
            lines[i] = line.replace('=== 0', '=== 0 || cint(event.target.value) < 0')
        elif target_line_2 in line:
            # Modify the second target line's error message
            lines[i] = line.replace('Column width cannot be zero.', 'Column width cannot be zero or negative value.')
        elif target_line_3 in line:
            # Modify the third target line's error message
            lines[i] = line.replace('<div class="hidden-xs edit-grid-row">${__("Edit")}</div>', '<div class="hidden-xs edit-grid-row">${__("View")}</div>')

    with open(input_file_path) as f:
        if '<div class="hidden-xs edit-grid-row">${__("View")}</div>' in f.read():
            return
        elif 'Column width cannot be zero or negative value.' in f.read():
            return
        elif 'if (cint(event.target.value) === 0) {' in f.read():
            return
    
    with open(input_file_path, 'w') as file:
        file.writelines(lines)

    print('frappe/frappe/public/js/frappe/form/grid_row.js modified')
    

def addi_sal_ret_bon():
    file_path = "{}/{}".format(BENCH_PATH,"/apps/hrms/hrms/payroll/doctype/retention_bonus/retention_bonus.py")
    
    with open(file_path, "r") as file:
        content = file.read()
    
    updated_content = content.replace('''additional_salary = self.get_additional_salary()
		if self.additional_salary:''', '''additional_salary = self.get_additional_salary()
		if additional_salary:''')

    with open(file_path) as f:
        if '''additional_salary = self.get_additional_salary()
		if additional_salary:''' in f.read():
            return
        
    with open(file_path, "w") as file:
        file.write(updated_content)
        print("Additional Salary bug fixing in Retention Bonus. Successfully Updated.")
    



def upload_malicious_pdf():
    file_path = "{}/{}".format(BENCH_PATH,"apps/frappe/frappe/handler.py")
    
    with open(file_path, "r") as file:
        content = file.read()
    
    updated_content = content.replace('''content = file.stream.read()''', '''content = file.stream.read()
		contents = content.decode().split()
		malicious_words = ["<</AA", "<</O", "<</S", "<</JS", "try {", "/JavaScript", "obj", "endobj"]
		for word in contents:
			if any(malicious_word in word for malicious_word in malicious_words):
				frappe.throw("File keeps malicious contents. File is not safe.")''')

    with open(file_path) as f:
        if '''content = file.stream.read()
		contents = content.decode().split()
		malicious_words = ["<</AA", "<</O", "<</S", "<</JS", "try {", "/JavaScript", "obj", "endobj"]
		for word in contents:
			if any(malicious_word in word for malicious_word in malicious_words):
				frappe.throw("File keeps malicious contents. File is not safe.")''' in f.read():
            return
        
    with open(file_path, "w") as file:
        file.write(updated_content)
        print("Upload Malicious File. Successfully Updated.")

def cross_site_scripting():
    file_path = "{}/{}".format(BENCH_PATH, "apps/frappe/frappe/handler.py")
    
    with open(file_path, "r") as file:
        content = file.read()
    
    updated_content = content.replace('''if cmd != "login":
		data = execute_cmd(cmd)''', '''if cmd and cmd != "login":
		try:
			data = execute_cmd(cmd)
		except frappe.exceptions.ValidationError as e:
			frappe.response["message"] = "Invalid command."
			frappe.response["exc"] = "Error"
			frappe.response["http_status_code"] = 401
			return build_response("json")''')

    with open(file_path) as f:
        if '''if cmd and cmd != "login":
		try:
			data = execute_cmd(cmd)
		except frappe.exceptions.ValidationError as e:
			frappe.response["message"] = "Invalid command."
			frappe.response["exc"] = "Error"
			frappe.response["http_status_code"] = 401
			return build_response("json")''' in f.read():
            return
        
    with open(file_path, "w") as file:
        file.write(updated_content)
        print("Cross Site Scripting. Successfully Updated.")

def login_password_encryption():
    file_path = "{}/{}".format(BENCH_PATH,"apps/frappe/frappe/templates/includes/login/login.js")
    
    with open(file_path, "r") as file:
        content = file.read()
    
    updated_content = content.replace('''$(".form-login").on("submit", function (event) {
		event.preventDefault();
		var args = {};
		args.cmd = "login";
		args.usr = frappe.utils.xss_sanitise(($("#login_email").val() || "").trim());
		args.pwd = $("#login_password").val();
		args.device = "desktop";
		if (!args.usr || !args.pwd) {
			frappe.msgprint('{{ _("Both login and password required") }}');
			return false;
		}
		login.call(args);
		return false;
	});''', '''$(".form-login").on("submit", function (event) {
		var site_name = document.location.origin.split('//')[1].split('.')[0];
		let url;
		if(site_name == 'localhost:8000'){
			site_url = 'http://localhost:8000/api/method/wsc.templates.rsa_algo.rsa_gen_key';
		}
		else{
			site_url = 'https://' + site_name + '.worldskillcenter.org/api/method/wsc.templates.rsa_algo.rsa_gen_key'
		}
		event.preventDefault();
		$.ajax({url: site_url, success: function(result){
		var args = {};
		args.cmd = "login";
		args.usr = frappe.utils.xss_sanitise(($("#login_email").val() || "").trim());
		args.pwd = $("#login_password").val();
		const publicKey = result.message['public_key_pem_date']
		function encryptWithRSA(plaintext) {
			const publicKeyObj = forge.pki.publicKeyFromPem(publicKey);
			const encrypted = publicKeyObj.encrypt(plaintext, 'RSA-OAEP', {
				md: forge.md.sha256.create()			
			});
			return forge.util.encode64(encrypted);
		}
		const plaintext = args.pwd;
		const encryptedData = encryptWithRSA(plaintext).toString("base64");
		args.pwd = encryptedData
		args.no=result.message['rsa_no']
		args.device = "desktop";
		if (!args.usr || !args.pwd) {
			frappe.msgprint('{{ _("Both login and password required") }}');
			return false;
		}
		login.call(args);
		return false;
	}});
});''')

    with open(file_path) as f:
        if '''$(".form-login").on("submit", function (event) {
		var site_name = document.location.origin.split('//')[1].split('.')[0];
		let url;
		if(site_name == 'localhost:8000'){
			site_url = 'http://localhost:8000/api/method/wsc.templates.rsa_algo.rsa_gen_key';
		}
		else{
			site_url = 'https://' + site_name + '.worldskillcenter.org/api/method/wsc.templates.rsa_algo.rsa_gen_key'
		}
		event.preventDefault();
		$.ajax({url: site_url, success: function(result){
		var args = {};
		args.cmd = "login";
		args.usr = frappe.utils.xss_sanitise(($("#login_email").val() || "").trim());
		args.pwd = $("#login_password").val();
		const publicKey = result.message['public_key_pem_date']
		function encryptWithRSA(plaintext) {
			const publicKeyObj = forge.pki.publicKeyFromPem(publicKey);
			const encrypted = publicKeyObj.encrypt(plaintext, 'RSA-OAEP', {
				md: forge.md.sha256.create()			
			});
			return forge.util.encode64(encrypted);
		}
		const plaintext = args.pwd;
		const encryptedData = encryptWithRSA(plaintext).toString("base64");
		args.pwd = encryptedData
		args.no=result.message['rsa_no']
		args.device = "desktop";
		if (!args.usr || !args.pwd) {
			frappe.msgprint('{{ _("Both login and password required") }}');
			return false;
		}
		login.call(args);
		return false;
	}});
});''' in f.read():
            return
        
    with open(file_path, "w") as file:
        file.write(updated_content)
        print("Login Password Encryption Successfully Updated.")

def login_password_decryption():
    file_path = "{}/{}".format(BENCH_PATH, "apps/frappe/frappe/auth.py")
    
    with open(file_path, "r") as file:
        content = file.read()
    
    updated_content = content.replace('''from frappe.core.doctype.user.user import User

		if not (user and pwd):
			user, pwd = frappe.form_dict.get("usr"), frappe.form_dict.get("pwd")
		if not (user and pwd):
			self.fail(_("Incomplete login details"), user=user)

		_raw_user_name = user
		user = User.find_by_credentials(user, pwd)

		if not user:
			self.fail("Invalid login credentials", user=_raw_user_name)

		# Current login flow uses cached credentials for authentication while checking OTP.
		# Incase of OTP check, tracker for auth needs to be disabled(If not, it can remove tracker history as it is going to succeed anyway)
		# Tracker is activated for 2FA incase of OTP.
		ignore_tracker = should_run_2fa(user.name) and ("otp" in frappe.form_dict)
		tracker = None if ignore_tracker else get_login_attempt_tracker(user.name)

		if not user.is_authenticated:
			tracker and tracker.add_failure_attempt()
			self.fail("Invalid login credentials", user=user.name)
		elif not (user.name == "Administrator" or user.enabled):
			tracker and tracker.add_failure_attempt()
			self.fail("User disabled or missing", user=user.name)
		else:
			tracker and tracker.add_success_attempt()
		self.user = user.name

	def force_user_to_reset_password(self):
		if not self.user:
			return

		if self.user in frappe.STANDARD_USERS:
			return False

		reset_pwd_after_days = cint(
			frappe.db.get_single_value("System Settings", "force_user_to_reset_password")
		)

		if reset_pwd_after_days:
			last_password_reset_date = (
				frappe.db.get_value("User", self.user, "last_password_reset_date") or today()
			)

			last_pwd_reset_days = date_diff(today(), last_password_reset_date)

			if last_pwd_reset_days > reset_pwd_after_days:
				return True

	def check_password(self, user, pwd):
		"""check password"""
		try:
			# returns user in correct case
			return check_password(user, pwd)
		except frappe.AuthenticationError:
			self.fail("Incorrect password", user=user)

	def fail(self, message, user=None):
		if not user:
			user = _("Unknown User")
		frappe.local.response["message"] = message
		add_authentication_log(message, user, status="Failed")
		frappe.db.commit()
		raise frappe.AuthenticationError

	def run_trigger(self, event="on_login"):
		for method in frappe.get_hooks().get(event, []):
			frappe.call(frappe.get_attr(method), login_manager=self)

	def validate_hour(self):
		"""check if user is logging in during restricted hours"""
		login_before = int(frappe.db.get_value("User", self.user, "login_before", ignore=True) or 0)
		login_after = int(frappe.db.get_value("User", self.user, "login_after", ignore=True) or 0)

		if not (login_before or login_after):
			return

		from frappe.utils import now_datetime

		current_hour = int(now_datetime().strftime("%H"))

		if login_before and current_hour >= login_before:
			frappe.throw(_("Login not allowed at this time"), frappe.AuthenticationError)

		if login_after and current_hour < login_after:
			frappe.throw(_("Login not allowed at this time"), frappe.AuthenticationError)

	def login_as_guest(self):
		"""login as guest"""
		self.login_as("Guest")

	def login_as(self, user):
		self.user = user
		self.post_login()

	def logout(self, arg="", user=None):
		if not user:
			user = frappe.session.user
		self.run_trigger("on_logout")

		if user == frappe.session.user:
			delete_session(frappe.session.sid, user=user, reason="User Manually Logged Out")
			self.clear_cookies()
		else:
			clear_sessions(user)

	def clear_cookies(self):
		clear_cookies()


class CookieManager:
	def __init__(self):
		self.cookies = {}
		self.to_delete = []

	def init_cookies(self):
		if not frappe.local.session.get("sid"):
			return

		# sid expires in 3 days
		expires = datetime.datetime.now() + datetime.timedelta(days=3)
		if frappe.session.sid:
			self.set_cookie("sid", frappe.session.sid, expires=expires, httponly=True)
		if frappe.session.session_country:
			self.set_cookie("country", frappe.session.session_country)

	def set_cookie(self, key, value, expires=None, secure=False, httponly=False, samesite="Lax"):
		if not secure and hasattr(frappe.local, "request"):
			secure = frappe.local.request.scheme == "https"

		# Cordova does not work with Lax
		if frappe.local.session.data.device == "mobile":
			samesite = None

		self.cookies[key] = {
			"value": value,
			"expires": expires,
			"secure": secure,
			"httponly": httponly,
			"samesite": samesite,
		}

	def delete_cookie(self, to_delete):
		if not isinstance(to_delete, (list, tuple)):
			to_delete = [to_delete]

		self.to_delete.extend(to_delete)

	def flush_cookies(self, response):
		for key, opts in self.cookies.items():
			response.set_cookie(
				key,
				quote((opts.get("value") or "").encode("utf-8")),
				expires=opts.get("expires"),
				secure=opts.get("secure"),
				httponly=opts.get("httponly"),
				samesite=opts.get("samesite"),
			)

		# expires yesterday!
		expires = datetime.datetime.now() + datetime.timedelta(days=-1)
		for key in set(self.to_delete):
			response.set_cookie(key, "", expires=expires)


@frappe.whitelist()
def get_logged_user():
	return frappe.session.user


def clear_cookies():
	if hasattr(frappe.local, "session"):
		frappe.session.sid = ""
	frappe.local.cookie_manager.delete_cookie(
		["full_name", "user_id", "sid", "user_image", "system_user"]
	)


def validate_ip_address(user):
	"""check if IP Address is valid"""
	from frappe.core.doctype.user.user import get_restricted_ip_list

	# Only fetch required fields - for perf
	user_fields = ["restrict_ip", "bypass_restrict_ip_check_if_2fa_enabled"]
	user_info = (
		frappe.get_cached_value("User", user, user_fields, as_dict=True)
		if not frappe.flags.in_test
		else frappe.db.get_value("User", user, user_fields, as_dict=True)
	)
	ip_list = get_restricted_ip_list(user_info)
	if not ip_list:
		return

	system_settings = (
		frappe.get_cached_doc("System Settings")
		if not frappe.flags.in_test
		else frappe.get_single("System Settings")
	)
	# check if bypass restrict ip is enabled for all users
	bypass_restrict_ip_check = system_settings.bypass_restrict_ip_check_if_2fa_enabled

	# check if two factor auth is enabled
	if system_settings.enable_two_factor_auth and not bypass_restrict_ip_check:
		# check if bypass restrict ip is enabled for login user
		bypass_restrict_ip_check = user_info.bypass_restrict_ip_check_if_2fa_enabled

	for ip in ip_list:
		if frappe.local.request_ip.startswith(ip) or bypass_restrict_ip_check:
			return

	frappe.throw(_("Access not allowed from this IP Address"), frappe.AuthenticationError)


def get_login_attempt_tracker(user_name: str, raise_locked_exception: bool = True):
	"""Get login attempt tracker instance.

	:param user_name: Name of the loggedin user
	:param raise_locked_exception: If set, raises an exception incase of user not allowed to login
	"""
	sys_settings = frappe.get_doc("System Settings")
	track_login_attempts = sys_settings.allow_consecutive_login_attempts > 0
	tracker_kwargs = {}

	if track_login_attempts:
		tracker_kwargs["lock_interval"] = sys_settings.allow_login_after_fail
		tracker_kwargs["max_consecutive_login_attempts"] = sys_settings.allow_consecutive_login_attempts

	tracker = LoginAttemptTracker(user_name, **tracker_kwargs)

	if raise_locked_exception and track_login_attempts and not tracker.is_user_allowed():
		frappe.throw(
			_("Your account has been locked and will resume after {0} seconds").format(
				sys_settings.allow_login_after_fail
			),
			frappe.SecurityException,
		)
	return tracker


class LoginAttemptTracker:
	"""Track login attemts of a user.

	Lock the account for s number of seconds if there have been n consecutive unsuccessful attempts to log in.
	"""

	def __init__(
		self, user_name: str, max_consecutive_login_attempts: int = 3, lock_interval: int = 5 * 60
	):
		"""Initialize the tracker.

		:param user_name: Name of the loggedin user
		:param max_consecutive_login_attempts: Maximum allowed consecutive failed login attempts
		:param lock_interval: Locking interval incase of maximum failed attempts
		"""
		self.user_name = user_name
		self.lock_interval = datetime.timedelta(seconds=lock_interval)
		self.max_failed_logins = max_consecutive_login_attempts

	@property
	def login_failed_count(self):
		return frappe.cache().hget("login_failed_count", self.user_name)

	@login_failed_count.setter
	def login_failed_count(self, count):
		frappe.cache().hset("login_failed_count", self.user_name, count)

	@login_failed_count.deleter
	def login_failed_count(self):
		frappe.cache().hdel("login_failed_count", self.user_name)

	@property
	def login_failed_time(self):
		"""First failed login attempt time within lock interval.

		For every user we track only First failed login attempt time within lock interval of time.
		"""
		return frappe.cache().hget("login_failed_time", self.user_name)

	@login_failed_time.setter
	def login_failed_time(self, timestamp):
		frappe.cache().hset("login_failed_time", self.user_name, timestamp)

	@login_failed_time.deleter
	def login_failed_time(self):
		frappe.cache().hdel("login_failed_time", self.user_name)''', '''import pymysql
		conn = pymysql.connect(
		host="localhost",
		user="erpnext",
		password="erp@123",
		database="erpdb"
		)

		c=conn.cursor()
		sql="select private_key_pem_date from `rsa_data` where name=%s AND flag=1 "%(frappe.form_dict.get('no'))
		c.execute(sql)
		ras_data = c.fetchall()
		c.close()
		# ras_data=frappe.db.sql("select private_key_pem_date from `rsa_data` where name='%s' AND flag='1' "%(frappe.form_dict.get('no')),as_dict=True)
		if ras_data:
				rsa_No = ras_data[0][0]
				# frappe.db.sql("Update `rsa_data` set flag='0' where name='%s' "%(frappe.form_dict.get('no')))
				sql="Update `rsa_data` set flag='0' where name='%s' "%(frappe.form_dict.get('no'))
				c=conn.cursor()
				c.execute(sql)
				conn.commit()
				c.close()
				import base64
				from cryptography.hazmat.primitives import serialization
				from cryptography.hazmat.primitives.asymmetric import rsa
				from cryptography.hazmat.primitives import hashes
				from cryptography.hazmat.primitives.asymmetric import padding
				private_key_pem=rsa_No
				#put the encrypted data received from the client side
				encrypted_data_base64 = frappe.form_dict.get("pwd")

				encrypted_data = base64.b64decode(encrypted_data_base64) # here it is converted into binary
				# creating the loaded private key
				loaded_private_key = serialization.load_pem_private_key(
						private_key_pem.encode(),
						password=None
						)
				# decoding
				decrypted_data = loaded_private_key.decrypt(
						encrypted_data,
						padding.OAEP(
								mgf=padding.MGF1(algorithm=hashes.SHA256()),
								algorithm=hashes.SHA256(),
								label=None
						)
				)
				# Print the decrypted data
				password=decrypted_data.decode()
				##################################### end of my code
				from frappe.core.doctype.user.user import User
				if not (user and pwd):
						user, pwd = frappe.form_dict.get("usr"), password
				if not (user and pwd):
						self.fail(_("Incomplete login details"), user=user)
				user = User.find_by_credentials(user, pwd)
				if not user:
						self.fail("Invalid login credentials")
		# Current login flow uses cached credentials for authentication while checking OTP.
		# Incase of OTP check, tracker for auth needs to be disabled(If not, it can remove tracker history as it is going to succeed anyway)
		# Tracker is activated for 2FA incase of OTP.
				ignore_tracker = should_run_2fa(user.name) and ("otp" in frappe.form_dict)
				tracker = None if ignore_tracker else get_login_attempt_tracker(user.name)
				if not user.is_authenticated:
						tracker and tracker.add_failure_attempt()
						self.fail("Invalid login credentials", user=user.name)
				elif not (user.name == "Administrator" or user.enabled):
						tracker and tracker.add_failure_attempt()
						self.fail("User disabled or missing", user=user.name)
				else:
						tracker and tracker.add_success_attempt()
				self.user = user.name
		else:
				frappe.throw("Bad Credentials Contact To Administrator")

	def force_user_to_reset_password(self):
		if not self.user:
			return

		if self.user in frappe.STANDARD_USERS:
			return False

		reset_pwd_after_days = cint(
			frappe.db.get_single_value("System Settings", "force_user_to_reset_password")
		)

		if reset_pwd_after_days:
			last_password_reset_date = (
				frappe.db.get_value("User", self.user, "last_password_reset_date") or today()
			)

			last_pwd_reset_days = date_diff(today(), last_password_reset_date)

			if last_pwd_reset_days > reset_pwd_after_days:
				return True

	def check_password(self, user, pwd):
		"""check password"""
		try:
			# returns user in correct case
			return check_password(user, pwd)
		except frappe.AuthenticationError:
			self.fail("Incorrect password", user=user)

	def fail(self, message, user=None):
		if not user:
			user = _("Unknown User")
		frappe.local.response["message"] = message
		add_authentication_log(message, user, status="Failed")
		frappe.db.commit()
		raise frappe.AuthenticationError

	def run_trigger(self, event="on_login"):
		for method in frappe.get_hooks().get(event, []):
			frappe.call(frappe.get_attr(method), login_manager=self)

	def validate_hour(self):
		"""check if user is logging in during restricted hours"""
		login_before = int(frappe.db.get_value("User", self.user, "login_before", ignore=True) or 0)
		login_after = int(frappe.db.get_value("User", self.user, "login_after", ignore=True) or 0)

		if not (login_before or login_after):
			return

		from frappe.utils import now_datetime

		current_hour = int(now_datetime().strftime("%H"))

		if login_before and current_hour >= login_before:
			frappe.throw(_("Login not allowed at this time"), frappe.AuthenticationError)

		if login_after and current_hour < login_after:
			frappe.throw(_("Login not allowed at this time"), frappe.AuthenticationError)

	def login_as_guest(self):
		"""login as guest"""
		self.login_as("Guest")

	def login_as(self, user):
		self.user = user
		self.post_login()

	def logout(self, arg="", user=None):
		if not user:
			user = frappe.session.user
		self.run_trigger("on_logout")

		if user == frappe.session.user:
			delete_session(frappe.session.sid, user=user, reason="User Manually Logged Out")
			self.clear_cookies()
		else:
			clear_sessions(user)

	def clear_cookies(self):
		clear_cookies()


class CookieManager:
	def __init__(self):
		self.cookies = {}
		self.to_delete = []

	def init_cookies(self):
		if not frappe.local.session.get("sid"):
			return

		# sid expires in 3 days
		expires = datetime.datetime.now() + datetime.timedelta(days=3)
		if frappe.session.sid:
			self.set_cookie("sid", frappe.session.sid, expires=expires, httponly=True)
		if frappe.session.session_country:
			self.set_cookie("country", frappe.session.session_country)

	def set_cookie(self, key, value, expires=None, secure=False, httponly=False, samesite="Lax"):
		if not secure and hasattr(frappe.local, "request"):
			secure = frappe.local.request.scheme == "https"

		# Cordova does not work with Lax
		if frappe.local.session.data.device == "mobile":
			samesite = None

		self.cookies[key] = {
			"value": value,
			"expires": expires,
			"secure": secure,
			"httponly": httponly,
			"samesite": samesite,
		}

	def delete_cookie(self, to_delete):
		if not isinstance(to_delete, (list, tuple)):
			to_delete = [to_delete]

		self.to_delete.extend(to_delete)

	def flush_cookies(self, response):
		for key, opts in self.cookies.items():
			response.set_cookie(
				key,
				quote((opts.get("value") or "").encode("utf-8")),
				expires=opts.get("expires"),
				secure=opts.get("secure"),
				httponly=opts.get("httponly"),
				samesite=opts.get("samesite"),
			)

		# expires yesterday!
		expires = datetime.datetime.now() + datetime.timedelta(days=-1)
		for key in set(self.to_delete):
			response.set_cookie(key, "", expires=expires)


@frappe.whitelist()
def get_logged_user():
	return frappe.session.user


def clear_cookies():
	if hasattr(frappe.local, "session"):
		frappe.session.sid = ""
	frappe.local.cookie_manager.delete_cookie(
		["full_name", "user_id", "sid", "user_image", "system_user"]
	)


def validate_ip_address(user):
	"""check if IP Address is valid"""
	from frappe.core.doctype.user.user import get_restricted_ip_list

	# Only fetch required fields - for perf
	user_fields = ["restrict_ip", "bypass_restrict_ip_check_if_2fa_enabled"]
	user_info = (
		frappe.get_cached_value("User", user, user_fields, as_dict=True)
		if not frappe.flags.in_test
		else frappe.db.get_value("User", user, user_fields, as_dict=True)
	)
	ip_list = get_restricted_ip_list(user_info)
	if not ip_list:
		return

	system_settings = (
		frappe.get_cached_doc("System Settings")
		if not frappe.flags.in_test
		else frappe.get_single("System Settings")
	)
	# check if bypass restrict ip is enabled for all users
	bypass_restrict_ip_check = system_settings.bypass_restrict_ip_check_if_2fa_enabled

	# check if two factor auth is enabled
	if system_settings.enable_two_factor_auth and not bypass_restrict_ip_check:
		# check if bypass restrict ip is enabled for login user
		bypass_restrict_ip_check = user_info.bypass_restrict_ip_check_if_2fa_enabled

	for ip in ip_list:
		if frappe.local.request_ip.startswith(ip) or bypass_restrict_ip_check:
			return

	frappe.throw(_("Access not allowed from this IP Address"), frappe.AuthenticationError)


def get_login_attempt_tracker(user_name: str, raise_locked_exception: bool = True):
	"""Get login attempt tracker instance.

	:param user_name: Name of the loggedin user
	:param raise_locked_exception: If set, raises an exception incase of user not allowed to login
	"""
	sys_settings = frappe.get_doc("System Settings")
	track_login_attempts = sys_settings.allow_consecutive_login_attempts > 0
	tracker_kwargs = {}

	if track_login_attempts:
		tracker_kwargs["lock_interval"] = sys_settings.allow_login_after_fail
		tracker_kwargs["max_consecutive_login_attempts"] = sys_settings.allow_consecutive_login_attempts

	tracker = LoginAttemptTracker(user_name, **tracker_kwargs)

	if raise_locked_exception and track_login_attempts and not tracker.is_user_allowed():
		frappe.throw(
			_("Your account has been locked and will resume after {0} seconds").format(
				sys_settings.allow_login_after_fail
			),
			frappe.SecurityException,
		)
	return tracker


class LoginAttemptTracker:
	"""Track login attemts of a user.

	Lock the account for s number of seconds if there have been n consecutive unsuccessful attempts to log in.
	"""

	def __init__(
		self, user_name: str, max_consecutive_login_attempts: int = 3, lock_interval: int = 5 * 60
	):
		"""Initialize the tracker.

		:param user_name: Name of the loggedin user
		:param max_consecutive_login_attempts: Maximum allowed consecutive failed login attempts
		:param lock_interval: Locking interval incase of maximum failed attempts
		"""
		self.user_name = user_name
		self.lock_interval = datetime.timedelta(seconds=lock_interval)
		self.max_failed_logins = max_consecutive_login_attempts

	@property
	def login_failed_count(self):
		return frappe.cache().hget("login_failed_count", self.user_name)

	@login_failed_count.setter
	def login_failed_count(self, count):
		frappe.cache().hset("login_failed_count", self.user_name, count)

	@login_failed_count.deleter
	def login_failed_count(self):
		frappe.cache().hdel("login_failed_count", self.user_name)

	@property
	def login_failed_time(self):
		"""First failed login attempt time within lock interval.

		For every user we track only First failed login attempt time within lock interval of time.
		"""
		return frappe.cache().hget("login_failed_time", self.user_name)

	@login_failed_time.setter
	def login_failed_time(self, timestamp):
		frappe.cache().hset("login_failed_time", self.user_name, timestamp)

	@login_failed_time.deleter
	def login_failed_time(self):
		frappe.cache().hdel("login_failed_time", self.user_name)''')

    with open(file_path) as f:
        if '''import pymysql
		conn = pymysql.connect(
		host="localhost",
		user="erpnext",
		password="erp@123",
		database="erpdb"
		)

		c=conn.cursor()
		sql="select private_key_pem_date from `rsa_data` where name=%s AND flag=1 "%(frappe.form_dict.get('no'))
		c.execute(sql)
		ras_data = c.fetchall()
		c.close()
		# ras_data=frappe.db.sql("select private_key_pem_date from `rsa_data` where name='%s' AND flag='1' "%(frappe.form_dict.get('no')),as_dict=True)
		if ras_data:
				rsa_No = ras_data[0][0]
				# frappe.db.sql("Update `rsa_data` set flag='0' where name='%s' "%(frappe.form_dict.get('no')))
				sql="Update `rsa_data` set flag='0' where name='%s' "%(frappe.form_dict.get('no'))
				c=conn.cursor()
				c.execute(sql)
				conn.commit()
				c.close()
				import base64
				from cryptography.hazmat.primitives import serialization
				from cryptography.hazmat.primitives.asymmetric import rsa
				from cryptography.hazmat.primitives import hashes
				from cryptography.hazmat.primitives.asymmetric import padding
				private_key_pem=rsa_No
				#put the encrypted data received from the client side
				encrypted_data_base64 = frappe.form_dict.get("pwd")

				encrypted_data = base64.b64decode(encrypted_data_base64) # here it is converted into binary
				# creating the loaded private key
				loaded_private_key = serialization.load_pem_private_key(
						private_key_pem.encode(),
						password=None
						)
				# decoding
				decrypted_data = loaded_private_key.decrypt(
						encrypted_data,
						padding.OAEP(
								mgf=padding.MGF1(algorithm=hashes.SHA256()),
								algorithm=hashes.SHA256(),
								label=None
						)
				)
				# Print the decrypted data
				password=decrypted_data.decode()
				##################################### end of my code
				from frappe.core.doctype.user.user import User
				if not (user and pwd):
						user, pwd = frappe.form_dict.get("usr"), password
				if not (user and pwd):
						self.fail(_("Incomplete login details"), user=user)
				user = User.find_by_credentials(user, pwd)
				if not user:
						self.fail("Invalid login credentials")
		# Current login flow uses cached credentials for authentication while checking OTP.
		# Incase of OTP check, tracker for auth needs to be disabled(If not, it can remove tracker history as it is going to succeed anyway)
		# Tracker is activated for 2FA incase of OTP.
				ignore_tracker = should_run_2fa(user.name) and ("otp" in frappe.form_dict)
				tracker = None if ignore_tracker else get_login_attempt_tracker(user.name)
				if not user.is_authenticated:
						tracker and tracker.add_failure_attempt()
						self.fail("Invalid login credentials", user=user.name)
				elif not (user.name == "Administrator" or user.enabled):
						tracker and tracker.add_failure_attempt()
						self.fail("User disabled or missing", user=user.name)
				else:
						tracker and tracker.add_success_attempt()
				self.user = user.name
		else:
				frappe.throw("Bad Credentials Contact To Administrator")

	def force_user_to_reset_password(self):
		if not self.user:
			return

		if self.user in frappe.STANDARD_USERS:
			return False

		reset_pwd_after_days = cint(
			frappe.db.get_single_value("System Settings", "force_user_to_reset_password")
		)

		if reset_pwd_after_days:
			last_password_reset_date = (
				frappe.db.get_value("User", self.user, "last_password_reset_date") or today()
			)

			last_pwd_reset_days = date_diff(today(), last_password_reset_date)

			if last_pwd_reset_days > reset_pwd_after_days:
				return True

	def check_password(self, user, pwd):
		"""check password"""
		try:
			# returns user in correct case
			return check_password(user, pwd)
		except frappe.AuthenticationError:
			self.fail("Incorrect password", user=user)

	def fail(self, message, user=None):
		if not user:
			user = _("Unknown User")
		frappe.local.response["message"] = message
		add_authentication_log(message, user, status="Failed")
		frappe.db.commit()
		raise frappe.AuthenticationError

	def run_trigger(self, event="on_login"):
		for method in frappe.get_hooks().get(event, []):
			frappe.call(frappe.get_attr(method), login_manager=self)

	def validate_hour(self):
		"""check if user is logging in during restricted hours"""
		login_before = int(frappe.db.get_value("User", self.user, "login_before", ignore=True) or 0)
		login_after = int(frappe.db.get_value("User", self.user, "login_after", ignore=True) or 0)

		if not (login_before or login_after):
			return

		from frappe.utils import now_datetime

		current_hour = int(now_datetime().strftime("%H"))

		if login_before and current_hour >= login_before:
			frappe.throw(_("Login not allowed at this time"), frappe.AuthenticationError)

		if login_after and current_hour < login_after:
			frappe.throw(_("Login not allowed at this time"), frappe.AuthenticationError)

	def login_as_guest(self):
		"""login as guest"""
		self.login_as("Guest")

	def login_as(self, user):
		self.user = user
		self.post_login()

	def logout(self, arg="", user=None):
		if not user:
			user = frappe.session.user
		self.run_trigger("on_logout")

		if user == frappe.session.user:
			delete_session(frappe.session.sid, user=user, reason="User Manually Logged Out")
			self.clear_cookies()
		else:
			clear_sessions(user)

	def clear_cookies(self):
		clear_cookies()


class CookieManager:
	def __init__(self):
		self.cookies = {}
		self.to_delete = []

	def init_cookies(self):
		if not frappe.local.session.get("sid"):
			return

		# sid expires in 3 days
		expires = datetime.datetime.now() + datetime.timedelta(days=3)
		if frappe.session.sid:
			self.set_cookie("sid", frappe.session.sid, expires=expires, httponly=True)
		if frappe.session.session_country:
			self.set_cookie("country", frappe.session.session_country)

	def set_cookie(self, key, value, expires=None, secure=False, httponly=False, samesite="Lax"):
		if not secure and hasattr(frappe.local, "request"):
			secure = frappe.local.request.scheme == "https"

		# Cordova does not work with Lax
		if frappe.local.session.data.device == "mobile":
			samesite = None

		self.cookies[key] = {
			"value": value,
			"expires": expires,
			"secure": secure,
			"httponly": httponly,
			"samesite": samesite,
		}

	def delete_cookie(self, to_delete):
		if not isinstance(to_delete, (list, tuple)):
			to_delete = [to_delete]

		self.to_delete.extend(to_delete)

	def flush_cookies(self, response):
		for key, opts in self.cookies.items():
			response.set_cookie(
				key,
				quote((opts.get("value") or "").encode("utf-8")),
				expires=opts.get("expires"),
				secure=opts.get("secure"),
				httponly=opts.get("httponly"),
				samesite=opts.get("samesite"),
			)

		# expires yesterday!
		expires = datetime.datetime.now() + datetime.timedelta(days=-1)
		for key in set(self.to_delete):
			response.set_cookie(key, "", expires=expires)


@frappe.whitelist()
def get_logged_user():
	return frappe.session.user


def clear_cookies():
	if hasattr(frappe.local, "session"):
		frappe.session.sid = ""
	frappe.local.cookie_manager.delete_cookie(
		["full_name", "user_id", "sid", "user_image", "system_user"]
	)


def validate_ip_address(user):
	"""check if IP Address is valid"""
	from frappe.core.doctype.user.user import get_restricted_ip_list

	# Only fetch required fields - for perf
	user_fields = ["restrict_ip", "bypass_restrict_ip_check_if_2fa_enabled"]
	user_info = (
		frappe.get_cached_value("User", user, user_fields, as_dict=True)
		if not frappe.flags.in_test
		else frappe.db.get_value("User", user, user_fields, as_dict=True)
	)
	ip_list = get_restricted_ip_list(user_info)
	if not ip_list:
		return

	system_settings = (
		frappe.get_cached_doc("System Settings")
		if not frappe.flags.in_test
		else frappe.get_single("System Settings")
	)
	# check if bypass restrict ip is enabled for all users
	bypass_restrict_ip_check = system_settings.bypass_restrict_ip_check_if_2fa_enabled

	# check if two factor auth is enabled
	if system_settings.enable_two_factor_auth and not bypass_restrict_ip_check:
		# check if bypass restrict ip is enabled for login user
		bypass_restrict_ip_check = user_info.bypass_restrict_ip_check_if_2fa_enabled

	for ip in ip_list:
		if frappe.local.request_ip.startswith(ip) or bypass_restrict_ip_check:
			return

	frappe.throw(_("Access not allowed from this IP Address"), frappe.AuthenticationError)


def get_login_attempt_tracker(user_name: str, raise_locked_exception: bool = True):
	"""Get login attempt tracker instance.

	:param user_name: Name of the loggedin user
	:param raise_locked_exception: If set, raises an exception incase of user not allowed to login
	"""
	sys_settings = frappe.get_doc("System Settings")
	track_login_attempts = sys_settings.allow_consecutive_login_attempts > 0
	tracker_kwargs = {}

	if track_login_attempts:
		tracker_kwargs["lock_interval"] = sys_settings.allow_login_after_fail
		tracker_kwargs["max_consecutive_login_attempts"] = sys_settings.allow_consecutive_login_attempts

	tracker = LoginAttemptTracker(user_name, **tracker_kwargs)

	if raise_locked_exception and track_login_attempts and not tracker.is_user_allowed():
		frappe.throw(
			_("Your account has been locked and will resume after {0} seconds").format(
				sys_settings.allow_login_after_fail
			),
			frappe.SecurityException,
		)
	return tracker


class LoginAttemptTracker:
	"""Track login attemts of a user.

	Lock the account for s number of seconds if there have been n consecutive unsuccessful attempts to log in.
	"""

	def __init__(
		self, user_name: str, max_consecutive_login_attempts: int = 3, lock_interval: int = 5 * 60
	):
		"""Initialize the tracker.

		:param user_name: Name of the loggedin user
		:param max_consecutive_login_attempts: Maximum allowed consecutive failed login attempts
		:param lock_interval: Locking interval incase of maximum failed attempts
		"""
		self.user_name = user_name
		self.lock_interval = datetime.timedelta(seconds=lock_interval)
		self.max_failed_logins = max_consecutive_login_attempts

	@property
	def login_failed_count(self):
		return frappe.cache().hget("login_failed_count", self.user_name)

	@login_failed_count.setter
	def login_failed_count(self, count):
		frappe.cache().hset("login_failed_count", self.user_name, count)

	@login_failed_count.deleter
	def login_failed_count(self):
		frappe.cache().hdel("login_failed_count", self.user_name)

	@property
	def login_failed_time(self):
		"""First failed login attempt time within lock interval.

		For every user we track only First failed login attempt time within lock interval of time.
		"""
		return frappe.cache().hget("login_failed_time", self.user_name)

	@login_failed_time.setter
	def login_failed_time(self, timestamp):
		frappe.cache().hset("login_failed_time", self.user_name, timestamp)

	@login_failed_time.deleter
	def login_failed_time(self):
		frappe.cache().hdel("login_failed_time", self.user_name)''' in f.read():
            return
        
    with open(file_path, "w") as file:
        file.write(updated_content)
        print("Login Password Decryption. Successfully Updated.")
    
def add_login_html_overrides():
    file_path = "{}/{}".format(BENCH_PATH,
                               "apps/frappe/frappe/www/login.html")
    with open(file_path, "r") as file:
        content = file.read()

    updated_content = content.replace('autocomplete="current-password"', 'onpaste="return false;"\tautocomplete="off"')

    with open(file_path) as f:
        if 'onpaste="return false;"\tautocomplete="off"' in f.read():
            return

    with open(file_path, "w") as file:
        file.write(updated_content)
        print("frappe/frappe/www/login.html modified onpaste='return false;' & autocomplete='off'.")

    # code_to_append = '\n<script src="https://cdnjs.cloudflare.com/ajax/libs/crypto-js/4.1.1/crypto-js.min.js" integrity="sha512-E8QSvWZ0eCLGk4km3hxSsNmGWbLtSCSUcewDQPQWZF6pEU8GlT8a5fF32wOl1i8ftdMhssTrF/OhyGWwonTcXA==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>'
    code_to_append = '/n<script src="https://cdnjs.cloudflare.com/ajax/libs/forge/0.10.0/forge.min.js"></script>'

    # Read the file content
    with open(file_path, 'r') as file:
        content = file.readlines()

    found_block_script = False

    with open(file_path) as f:
        if code_to_append in f.read():
            return

    # Search for {% block script %} and append the code if it's not already present
    for i, line in enumerate(content):
        if '{% block script %}' in line:
            found_block_script = True
            if code_to_append not in content[i+1]:
                content[i] = line.rstrip('\r\n')  # Remove trailing newline characters
                content.insert(i+1, code_to_append + '\n')  # Insert the code below {% block script %}
                with open(file_path, 'w') as file:
                    file.writelines(content)
                print("Add Login HTML. Successfully Updated.")
            # else:
            #     print("Code is already present in the file.")
            break

    # if not found_block_script:
    #     print("{% block script %} not found in the file.")

def insecure_transmission_password():
    file_path = "{}/{}".format(BENCH_PATH,"sites/assets/frappe/js/frappe/form/controls/password.js")
    
    with open(file_path, "r") as file:
        content = file.read()
    
    updated_content = content.replace('''var me = this;
		frappe.call({
			type: "POST",
			method: "frappe.core.doctype.user.user.test_password_strength",
			args: {
				new_password: value || "",''', '''var plain_password = ''
        for (let i = 0; i < value.length; i++) {
              plain_password += '*'
          }
		var me = this;
		frappe.call({
			type: "POST",
			method: "frappe.core.doctype.user.user.test_password_strength",
			args: {
				new_password: plain_password || "",''')

    with open(file_path) as f:
        if '''var plain_password = ''
        for (let i = 0; i < value.length; i++) {
              plain_password += '*'
          }
		var me = this;
		frappe.call({
			type: "POST",
			method: "frappe.core.doctype.user.user.test_password_strength",
			args: {
				new_password: plain_password || "",''' in f.read():
            return
        
    with open(file_path, "w") as file:
        file.write(updated_content)
        print("Insecure Password Transmission. Successfully Updated.")

def improper_error_handling_response():
    file_path = "{}/{}".format(BENCH_PATH,"apps/frappe/frappe/utils/response.py")
    
    with open(file_path, "r") as file:
        content = file.read()
    
    updated_content = content.replace('''def make_logs(response=None):
	"""make strings for msgprint and errprint"""
	if not response:
		response = frappe.local.response

	if frappe.error_log:
		response["exc"] = json.dumps([frappe.utils.cstr(d["exc"]) for d in frappe.local.error_log])

	if frappe.local.message_log:
		response["_server_messages"] = json.dumps(
			[frappe.utils.cstr(d) for d in frappe.local.message_log]
		)

	if frappe.debug_log and frappe.conf.get("logging") or False:
		response["_debug_messages"] = json.dumps(frappe.local.debug_log)

	if frappe.flags.error_message:
		response["_error_message"] = frappe.flags.error_message''', '''def make_logs(response=None):
	"""make strings for msgprint and errprint"""
	if not response:
		response = frappe.local.response

	if frappe.error_log:
		response["exc"] = "Authentication Error"

	if frappe.local.message_log:
		response["_server_messages"] = "Invalid command or command not allowed."

	if frappe.debug_log and frappe.conf.get("logging") or False:
		response["_debug_messages"] = "Authentication Error"

	if frappe.flags.error_message:
		response["_error_message"] = "Authentication Error"''')

    with open(file_path) as f:
        if '''def make_logs(response=None):
	"""make strings for msgprint and errprint"""
	if not response:
		response = frappe.local.response

	if frappe.error_log:
		response["exc"] = "Authentication Error"

	if frappe.local.message_log:
		response["_server_messages"] = "Invalid command or command not allowed."

	if frappe.debug_log and frappe.conf.get("logging") or False:
		response["_debug_messages"] = "Authentication Error"

	if frappe.flags.error_message:
		response["_error_message"] = "Authentication Error"''' in f.read():
            return
        
    with open(file_path, "w") as file:
        file.write(updated_content)
        print("Improper Error Handling Response. Successfully Updated.")

def process_response_website_js_1():
    file_path = "{}/{}".format(BENCH_PATH,"/apps/frappe/frappe/website/js/website.js")
    
    with open(file_path, "r") as file:
        content = file.read()
    
    updated_content = content.replace('''statusCode: opts.statusCode || {
				404: function () {
					frappe.msgprint(__("Not found"));
				},
				403: function () {
					frappe.msgprint(__("Not permitted"));
				},
				200: function (data) {
					if (opts.callback) opts.callback(data);
					if (opts.success) opts.success(data);
				},
			},''', '''statusCode: opts.statusCode || {
				404: function () {
					frappe.msgprint(__("Not found"));
				},
				403: function () {
					frappe.msgprint(__("Not permitted"));
				},
				200: function (data) {
					if (opts.callback) opts.callback(data);
					if (opts.success) opts.success(data);
				},
				401: function () {
					frappe.msgprint(__("Invalid Login/Password"));
				},
			},''')

    with open(file_path) as f:
        if '''statusCode: opts.statusCode || {
				404: function () {
					frappe.msgprint(__("Not found"));
				},
				403: function () {
					frappe.msgprint(__("Not permitted"));
				},
				200: function (data) {
					if (opts.callback) opts.callback(data);
					if (opts.success) opts.success(data);
				},
				401: function () {
					frappe.msgprint(__("Invalid Login/Password"));
				},
			},''' in f.read():
            return
        
    with open(file_path, "w") as file:
        file.write(updated_content)
        print("Process Response Website JS 1. Successfully Updated.")


def process_response_website_js_2():
    file_path = "{}/{}".format(BENCH_PATH,"/apps/frappe/frappe/website/js/website.js")
    
    with open(file_path, "r") as file:
        content = file.read()
    
    updated_content = content.replace('''if (data.responseText) {
				try {
					data = JSON.parse(data.responseText);
				} catch (e) {
					data = {};
				}
			}
			frappe.process_response(opts, data);''', '''// if (data.responseText) {
			// 	try {
			// 		data = JSON.parse(data.responseText);
			// 	} catch (e) {
			// 		data = {};
			// 	}
			// }
			// frappe.process_response(opts, data);''')

    with open(file_path) as f:
        if '''// if (data.responseText) {
			// 	try {
			// 		data = JSON.parse(data.responseText);
			// 	} catch (e) {
			// 		data = {};
			// 	}
			// }
			// frappe.process_response(opts, data);''' in f.read():
            return
        
    with open(file_path, "w") as file:
        file.write(updated_content)
        print("Process Response Website JS 2. Successfully Updated.")
        
def change_password_confirmation_1():
    file_path = "{}/{}".format(BENCH_PATH,"/apps/frappe/frappe/core/doctype/user/user.js")
    
    with open(file_path, "r") as file:
        content = file.read()
    
    updated_content = content.replace('''let doc = frm.doc;''', '''frm.set_value("new_password", '');
        frm.set_value("confirm_new_password", '');
		let doc = frm.doc;''')

    with open(file_path) as f:
        if '''frm.set_value("new_password", '');
        frm.set_value("confirm_new_password", '');
		let doc = frm.doc;''' in f.read():
            return
        
    with open(file_path, "w") as file:
        file.write(updated_content)
        print("Change Password Confirmation 1. Successfully Updated.")
        
def change_password_confirmation_2():
    file_path = "{}/{}".format(BENCH_PATH,"/apps/frappe/frappe/core/doctype/user/user.js")
    
    with open(file_path, "r") as file:
        content = file.read()
    
    updated_content = content.replace('''validate: function (frm) {
		if (frm.roles_editor) {
			frm.roles_editor.set_roles_in_table();
		}
	},''', '''validate: function (frm) {
		if (frm.roles_editor) {
			frm.roles_editor.set_roles_in_table();
		}
		if (frm.doc.new_password != frm.doc.confirm_new_password) {
            frappe.throw("Please set same value for <b>Set New Password</b> and <b>Confirm New Password</b>");
        }
	},''')

    with open(file_path) as f:
        if '''validate: function (frm) {
		if (frm.roles_editor) {
			frm.roles_editor.set_roles_in_table();
		}
		if (frm.doc.new_password != frm.doc.confirm_new_password) {
            frappe.throw("Please set same value for <b>Set New Password</b> and <b>Confirm New Password</b>");
        }
	},''' in f.read():
            return
        
    with open(file_path, "w") as file:
        file.write(updated_content)
        print("Change Password Confirmation 2. Successfully Updated.")
        

def update_forgot_password():
    file_path = "{}/{}".format(BENCH_PATH,"/apps/frappe/frappe/www/update-password.html")
    
    with open(file_path, "r") as file:
        content = file.read()
    
    updated_content = content.replace('''if (!args.new_password) {
			set_strength_indicator('grey', {'warning': "{{ _('Please enter the password') }}" });
			return;
		}''', '''if (!args.new_password) {
			set_strength_indicator('grey', {'warning': "{{ _('Please enter the password') }}" });
			return;
		}
		var plaintext = ''
		for (var i = 0; i < args.new_password.length; i++){
			plaintext += "*"
		}
		args.old_password = plaintext
		args.new_password = plaintext''')

    with open(file_path) as f:
        if '''if (!args.new_password) {
			set_strength_indicator('grey', {'warning': "{{ _('Please enter the password') }}" });
			return;
		}
		var plaintext = ''
		for (var i = 0; i < args.new_password.length; i++){
			plaintext += "*"
		}
		args.old_password = plaintext
		args.new_password = plaintext''' in f.read():
            return
        
    with open(file_path, "w") as file:
        file.write(updated_content)
        print("Update Forgot Password. Successfully Updated.")

def login_senetize_handle():
    file_path = "{}/{}".format(BENCH_PATH,"apps/frappe/frappe/handler.py")
    with open(file_path, "r") as file:
        content = file.read()
    updated_content = content.replace('''try:
		method = get_attr(cmd)
	except Exception as e:
		frappe.throw(_("Failed to get method for command {0} with {1}").format(cmd, e))''', '''try:
		special_characters = """@'!$%^&*()<>?/\|}{~:"#"""
		if any(spc in cmd for spc in special_characters):
			frappe.throw("Failed to get method for command {0} with {1}").format(cmd, e)
		else:
			method = get_attr(cmd)
	except Exception as e:
		frappe.throw(_("Failed to get method for command {0} with {1}").format(cmd, e))''')
    with open(file_path) as f:
        if '''try:
		special_characters = """@'!$%^&*()<>?/\|}{~:"#"""
		if any(spc in cmd for spc in special_characters):
			frappe.throw("Failed to get method for command {0} with {1}").format(cmd, e)
		else:
			method = get_attr(cmd)
	except Exception as e:
		frappe.throw(_("Failed to get method for command {0} with {1}").format(cmd, e))''' in f.read():
            return
    with open(file_path, "w") as file:
        file.write(updated_content)
        print("Login Senetize Handle. Successfully Updated.")

			
