import json
import traceback
import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
# from django.views.decorators.csrf import csrf_exempt
from wsgiref.util import FileWrapper

from . import utils, tasks
from .exceptions import *
from .form import StudentForm

# @csrf_exempt
@require_http_methods(["POST", "GET"])
def add_geocodes_to_addresses(request):
    if request.method == "GET":
        student = StudentForm()
        return render(request, "index.html", {'form':student})

    try:
        uploaded_file = request.FILES["input_file"]

        # Check if the uploaded file is an xlsx file
        uploaded_filename = uploaded_file.name
        if not uploaded_filename.endswith(".xlsx"):
            raise ValidationError("filetype", "is not '.xlsx'")

        # Add a timestamp tag to filename before saving to disk
        tagged_filename = utils.tag_timestamp(uploaded_filename)
        uploaded_filepath = utils.create_file_on_disk("uploaded_files", tagged_filename, uploaded_file, "request")

        # Read the xl file
        xl = pd.ExcelFile(uploaded_filepath)

        # Check if the xlsx file is in the desired format
        df = tasks.validate_input_file_and_get_df(xl)

        # Add geocodes
        tasks.add_geocodes(df)

        # Save the updated df back to a xlsx file on disk
        processed_filepath = utils.create_file_on_disk("processed_files", tagged_filename, df, "dataframe")

        # Return the updated xl file
        doc = open(processed_filepath, 'rb')
        response = HttpResponse(FileWrapper(doc), content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename="%s"' % uploaded_filename
        return response
    except KeyError:
        return HttpResponse(json.dumps({
                                       "msg":"Missing parameter (input_file) in the request."
                                       }
                                       ),status=400)
    except ValidationError as err:
        return HttpResponse(json.dumps({
                                       "msg":"Validation failed | " + err.validation + " - " + err.message
                                       }
                                       ),status=400)
    except FileNotFoundError:
        return HttpResponse(json.dumps({
                                       "msg":"Missing dirs (uploaded_files and/or processed_files) on server."
                                       }
                                       ),status=500)
    except Exception as err:
        traceback.print_exc()
        return HttpResponse(json.dumps({
                                       "msg":"Error occured during adding geocodes - " + str(err)
                                       }
                                       ),status=500)
