from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.set_font('Arial', '', 16)
pdf.cell(40, 10, '¡Hola mundo!')
pdf.output('prueba.pdf')