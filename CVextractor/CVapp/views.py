from django.shortcuts import render
# Create your views here.
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import CV
from .forms import CVUploadForm
from .utils import extract_information_from_cv
import xlwt
from django.http import HttpResponse
from .models import CV
import openpyxl

def upload_cv(request):
    if request.method == 'POST':
        form = CVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            cv_file = form.cleaned_data['cv_file']
            email, contact_number, overall_text = extract_information_from_cv(cv_file)
            cv = CV.objects.create(email=email, contact_number=contact_number, overall_text=overall_text)
            return HttpResponseRedirect('/success/')  # Redirect to success page after processing
    else:
        form = CVUploadForm(),
    return render(request, 'upload.html', {'form': form})

def success(request):
    return render(request, 'success.html')

def download_cv_data_as_excel(request):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="cv_data.xlsx"'

    # Retrieve CV data from the database
    cvs = CV.objects.all()

    # Create a new Excel workbook and worksheet
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'CV Data'

    # Write headers
    worksheet['A1'] = 'Email'
    worksheet['B1'] = 'Contact Number'
    worksheet['C1'] = 'Overall Text'

    # Write CV data to the worksheet
    for index, cv in enumerate(cvs, start=2):
        worksheet[f'A{index}'] = cv.email
        worksheet[f'B{index}'] = cv.contact_number
        worksheet[f'C{index}'] = cv.overall_text

    # Save the workbook to the response
    workbook.save(response)
    return response