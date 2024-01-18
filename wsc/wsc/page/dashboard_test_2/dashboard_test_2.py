import frappe

@frappe.whitelist()
def get_data():
    print("\n\n\n")
    print(frappe.session.user)
    # data_attendance = frappe.get_list("Student Attendance" , {'owner':frappe.session.user} , ['owner' , 'name'])
    data_attendance_present = frappe.db.sql("""
       SELECT 
            atten.owner, 
            atten.name, 
            COUNT(atten.name) as count_atten,
            atten.date, 
            atten.course_schedule ,
            class.name 
        FROM 
            `tabStudent Attendance` atten 
            INNER JOIN 
            `tabCourse Schedule` class 
            ON atten.course_schedule = class.name 
        WHERE
            atten.owner = "{email}" AND
            atten.status = "Present" AND
            atten.docstatus = 1
        GROUP BY atten.course_schedule 
    """.format(email = frappe.session.user) , as_dict=1)
    
    data_attendance_absent = frappe.db.sql("""
        SELECT 
            atten.owner, 
            atten.name, 
            COUNT(atten.name) as count_atten , 
            atten.date, 
            atten.course_schedule ,
            class.name 
        FROM 
            `tabStudent Attendance` atten
        INNER JOIN 
            `tabCourse Schedule` class
        ON atten.course_schedule = class.name 
        WHERE 
            atten.owner = "{email}" AND
            atten.status="Absent" AND
            atten.docstatus = 1
        GROUP BY atten.course_schedule
    """.format(email = frappe.session.user) , as_dict=1)
    
    data = frappe.db.sql("""
        SELECT      
            owner,     
            name,     
            date,     
            course_schedule,     
            (SELECT 
                COUNT(name) 
            FROM 
                `tabStudent Attendance` 
            WHERE 
                status = 'Present' AND
                owner = '{email}' AND 
                docstatus = 1 AND
                course_schedule = a.course_schedule) AS PresentCount ,
            (SELECT 
                COUNT(name) 
            FROM 
                `tabStudent Attendance` 
            WHERE 
                status = "Absent" AND
                owner = "{email}" AND
                docstatus = 1 AND
                course_schedule = a.course_schedule) AS AbsentCount 
            FROM      
            `tabStudent Attendance` a 
            WHERE     
            owner = 'trainer@gmail.com' AND
            docstatus = 1 
            GROUP BY course_schedule;    
    """.format(email = frappe.session.user) , as_dict= 1)

    print(data)
    # frappe.get_list
    return data