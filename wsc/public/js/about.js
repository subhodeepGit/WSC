frappe.provide("frappe.ui.misc");

frappe.ui.misc.about = function () {
	if (!frappe.ui.misc.about_dialog) {
		var d = new frappe.ui.Dialog({ title: __("Sustainable Outreach And Universal Leadership Limited") });

		$(d.body).html(
			repl(
				"<div>\
		<p>" +
					__("This Application is developed by SOUL Ltd. for WSC.") +
					"</p>  \
		<p><i class='fa fa-globe fa-fw'></i>\
			Website: <a href='https://soulunileaders.com/' target='_blank'>https://soulunileaders.com/</a></p>\
		<p><i class='fa fa-github fa-fw'></i>\
			Source: <a href='#' target='_blank'>https://github.com</a></p>\
		<p><i class='fa fa-linkedin fa-fw'></i>\
			Linkedin: <a href='https://www.linkedin.com/company/soullimited/' target='_blank'>https://www.linkedin.com/company/soullimited/</a></p>\
		<p><i class='fa fa-facebook fa-fw'></i>\
			Facebook: <a href='#' target='_blank'>https://facebook.com/</a></p>\
		<p><i class='fa fa-twitter fa-fw'></i>\
			Twitter: <a href='https://twitter.com/soul_limited' target='_blank'>https://twitter.com/soul_limited</a></p>\
        <p><i class='fa fa-envelope fa-fw'></i>\
            Email: <a href='mailto:soul@soulunileaders.com'> soul@soulunileaders.com</a></p>\
		<hr>\
		<h4>Installed Apps</h4>\
		<div id='about-app-versions'>Loading versions...</div>\
		<hr>\
		<p class='text-muted'>&copy; SOUL Ltd. and contributors </p> \
		</div>",
				frappe.app
			)
		);

		frappe.ui.misc.about_dialog = d;

		frappe.ui.misc.about_dialog.on_page_show = function () {
			if (!frappe.versions) {
				frappe.call({
					method: "frappe.utils.change_log.get_versions",
					callback: function (r) {
						show_versions(r.message);
					},
				});
			} else {
				show_versions(frappe.versions);
			}
		};

		var show_versions = function (versions) {
			var $wrap = $("#about-app-versions").empty();
			$.each(Object.keys(versions).sort(), function (i, key) {
				var v = versions[key];
				if (v.branch) {
                    if (v.title=="ERPNext"){
                        var text = $.format("<p><b>ERP:</b> v{0} ({1})<br></p>", [
                            v.branch_version || v.version,
                            v.branch,
                        ]);
                    }else if(v.title=="Frappe HR"){
                        var text = $.format("<p><b>HRMS:</b> v{0} ({1})<br></p>", [
                            v.branch_version || v.version,
                            v.branch,
                        ]);
                    }else{
                        var text = $.format("<p><b>{0}:</b> v{1} ({2})<br></p>", [
                            v.title,
                            v.branch_version || v.version,
                            v.branch,
                    ]);}
				} else {
					var text = $.format("<p><b>{0}:</b> v{1}<br></p>", [v.title, v.version]);
				}
				$(text).appendTo($wrap);
			});

			frappe.versions = versions;
		};
	}

	frappe.ui.misc.about_dialog.show();
};
