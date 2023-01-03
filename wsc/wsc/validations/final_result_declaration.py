from wsc.wsc.utils import academic_term, semester_belongs_to_programs

def validate(doc, method):
	academic_term(doc)
	semester_belongs_to_programs(doc)