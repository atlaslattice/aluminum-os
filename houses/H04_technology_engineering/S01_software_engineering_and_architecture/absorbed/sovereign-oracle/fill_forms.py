
import pdfrw

ANNOT_KEY = '/Annots'
ANNOT_FIELD_KEY = '/T'
ANNOT_VAL_KEY = '/V'
ANNOT_RECT_KEY = '/Rect'
SUBTYPE_KEY = '/Subtype'
WIDGET_SUBTYPE_KEY = '/Widget'


def fill_pdf(input_pdf_path, output_pdf_path, data_dict):
    template_pdf = pdfrw.PdfReader(input_pdf_path)
    for page in template_pdf.pages:
        annotations = page[ANNOT_KEY]
        if annotations:
            for annotation in annotations:
                if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
                    if annotation[ANNOT_FIELD_KEY]:
                        key = annotation[ANNOT_FIELD_KEY][1:-1]
                        if key in data_dict:
                            if type(data_dict[key]) == bool:
                                if data_dict[key] == True:
                                    annotation.update(pdfrw.PdfDict(AS=pdfrw.PdfName('Yes')))
                            else:
                                annotation.update(
                                    pdfrw.PdfDict(V='{}'.format(data_dict[key]))
                                )
                                annotation.update(pdfrw.PdfDict(AS=pdfrw.PdfName(''))) # update appearance stream

    template_pdf.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))
    pdfrw.PdfWriter().write(output_pdf_path, template_pdf)


# Form 26 Data
form26_data = {
    'Court Address': '1437 Bannock St., Room 256, Denver, CO 80202',
    'Plaintiff': 'Sheldon',
    'Defendant': 'John O\'Connor & Alex Knuckey',
    'Case Number': '25S00165',
    'Original Judgment': '8081.48',
    'Interest': '371.97',
    'Total Amount': '8453.45',
    'Payable to': 'Clerk of the Court',
    'Garnishee Name and Address': '', # To be filled in later
}

fill_pdf('/home/ubuntu/nova_shred/forms/Form26_Writ_Continuing_Garnishment.pdf', '/home/ubuntu/nova_shred/filled_forms/Form26_filled.pdf', form26_data)

# Form 29 Data
form29_data = {
    'Court Address': '1437 Bannock St., Room 256, Denver, CO 80202',
    'Plaintiff': 'Sheldon',
    'Defendant': 'John O\'Connor & Alex Knuckey',
    'Case Number': '25S00165',
    'Original Judgment': '8081.48',
    'Interest': '371.97',
    'Total Amount': '8453.45',
    'Payable to': 'Clerk of the Court',
    'Garnishee Name and Address': '', # To be filled in later
}

fill_pdf('/home/ubuntu/nova_shred/forms/Form29_Writ_Garnishment_Bank.pdf', '/home/ubuntu/nova_shred/filled_forms/Form29_filled.pdf', form29_data)


print('Garnishment forms filled successfully!')
