from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def render_invoice_pdf(order):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    pdf.setTitle(f'Invoice {order.order_number}')
    pdf.setFont('Helvetica-Bold', 18)
    pdf.drawString(40, 800, f'Invoice #{order.order_number}')
    pdf.setFont('Helvetica', 11)
    pdf.drawString(40, 775, f'Customer: {order.user.get_full_name() or order.user.username}')
    pdf.drawString(40, 755, f'Status: {order.status.title()}')
    y = 720
    for item in order.items.all():
        pdf.drawString(40, y, f'{item.name} x {item.quantity}')
        pdf.drawRightString(550, y, f'Rs. {item.line_total}')
        y -= 22
    pdf.setFont('Helvetica-Bold', 12)
    pdf.drawRightString(550, y - 20, f'Total: Rs. {order.grand_total}')
    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    return buffer
