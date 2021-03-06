from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper
import os
import utilities


# -- coding: utf-8--

# helper controller for fetching the WaterML file
def temp_waterml(request, id):
    print "hello"
    base_path = utilities.get_workspace()
    file_path = base_path + "/" +id
    response = HttpResponse(FileWrapper(open(file_path)), content_type='application/xml')
    return response


# formats the time series for highcharts
def chart_data(request, res_id):
    print"chart data"
    print res_id
    # checks if we already have an unzipped xml file
    file_path = utilities.waterml_file_path(res_id)

    # if we don't have the xml file, downloads and unzips it
    if not os.path.exists(file_path):
        utilities.unzip_waterml(request, res_id)

    # returns an error message if the unzip_waterml failed
    if not os.path.exists(file_path):
        data_for_chart = {'status': 'Resource file not found'}
    else:
        # parses the WaterML to a chart data object
        data_for_chart = utilities.Original_Checker(file_path)

    return JsonResponse(data_for_chart)


# home page controller
def home(request):

    return render(request, 'timeseries_viewer/home.html', {})