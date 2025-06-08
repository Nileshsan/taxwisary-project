import json
from django.http import JsonResponse
from django.db import transaction
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from cloudinary.uploader import upload
from datetime import datetime
import logging

from .models import TempUserData, TempIncomeDetails, TaxReport, UserProfile

logger = logging.getLogger(__name__)

def generate_report(request, temp_data):
    try:
        with transaction.atomic():
            # Create or update the basic user data record using TempUserData model.
            basic_data = TempUserData.objects.create(
                user=request.user,
                full_name=temp_data.get('full_name', '').strip(),
                dob=temp_data.get('dob', '2000-01-01'),
                phone=temp_data.get('phone', '').strip(),
                email=temp_data.get('email', '').strip(),
                # Include other fields as needed
            )
            
            # Merge any additional data if needed
            merged_data = {
                'id': basic_data.id,
                'full_name': basic_data.full_name,
                'dob': basic_data.dob,
                'phone': basic_data.phone,
                'email': basic_data.email,
                # Merge any other data from temp_data
            }
            
            file_name = f"tax_report_{request.user.username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            template = get_template('users/report.html')
            context = {
                'user': request.user,
                'temp_data': merged_data,
                'generated_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            html = template.render(context)
            result = BytesIO()
            pdf = pisa.CreatePDF(BytesIO(html.encode("UTF-8")), dest=result)
            if pdf.err:
                raise Exception("PDF generation error.")
            result.seek(0)
            
            cloudinary_response = upload(result, resource_type="raw", public_id=file_name, folder="tax_reports")
            secure_url = cloudinary_response.get("secure_url")
            if not secure_url:
                raise Exception("Failed to get secure URL from Cloudinary")
            
            basic_data.pdf_url = secure_url
            basic_data.save()
            
            # Create a TaxReport record.
            TaxReport.objects.create(user=request.user, pdf_url=secure_url)
            
            # Optionally, update UserProfile with the basic data.
            UserProfile.objects.update_or_create(
                user=request.user,
                defaults={
                    'full_name': basic_data.full_name,
                    'dob': basic_data.dob,
                    'phone': basic_data.phone,
                    'email': basic_data.email,
                }
            )
            
            logger.info(f"PDF generated successfully: {secure_url}")
            return JsonResponse({"response": secure_url})
    except Exception as e:
        logger.error(f"Error in generate_report: {str(e)}")
        return JsonResponse({"error": "Error generating report"}, status=500)