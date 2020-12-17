import datetime

from docxtpl import DocxTemplate

doc = DocxTemplate("data/templates/Birth_of_a_child_eng.docx")
context = {'name': "World company",
           'date': datetime.datetime.now().strftime('%d.%m.%Y')}
doc.render(context)
doc.save("data/templates/generated_doc.doc")