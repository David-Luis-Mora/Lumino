import os

from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django_rq import job
from weasyprint import HTML


def deliver_certificate(base_url, student):
    # Generar el PDF dinámicamente
    output_path = os.path.join(
        settings.MEDIA_ROOT, 'certificates', f'{student.username}_grade_certificate.pdf'
    )

    # Crea la carpeta de certificados si no existe
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Generar el contenido HTML para el PDF
    html_string = render_to_string('subjects/certificate_template.html', {'student': student})
    pdf = HTML(string=html_string, base_url=base_url).write_pdf()

    # Guardar el PDF
    with open(output_path, 'wb') as f:
        f.write(pdf)

    # Enviar el correo con el certificado adjunto
    email = EmailMessage(
        subject='Your Grade Certificate',
        body=f'Dear {student.first_name},\n\nPlease find attached your grade certificate.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[student.email],
    )
    email.attach_file(output_path)
    email.send()


@job
def heavy_processing():
    pass
