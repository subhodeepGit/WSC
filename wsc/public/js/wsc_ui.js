$(document).ready(function () {
    let proFileRole = null
    if (frappe.session.user != 'Guest') {
        frappe.model.get_value('User', { 'name': frappe.session.user }, "role_profile_name",
            (role) => {
                // Update Header Images
                proFileRole = role.role_profile_name
                frappe.model.get_value('Site Settings', { 'name': 'Site Settings' }, '*',
                    (settings) => {
                        // console.log(proFileRole)
                        // console.log(settings)
                        if (proFileRole === 'Student Role') {
                            const style = document.createElement('style');
                            style.innerHTML = `
                                header.navbar,
                                nav.navbar.navbar-expand-lg {
                                    background-image: url(${settings.student_background})  !important;
                                }
                                .layout-side-section{display: none;}
                                `;
                            document.head.appendChild(style);
                        } else if (proFileRole === 'Employee Role') {
                            const style = document.createElement('style');
                            style.innerHTML = `
                            header.navbar,
                            nav.navbar.navbar-expand-lg {
                                background-image: url(${settings.employee_background}) !important;
                            }
                            `;
                            document.head.appendChild(style);
                        } else {
                            const style = document.createElement('style');
                            style.innerHTML = `
                            header.navbar,
                            nav.navbar.navbar-expand-lg {
                                background-image: url(${settings.main_background})  !important;
                            }
                            `;
                            document.head.appendChild(style);
                        }
                    })
            })

    }
})