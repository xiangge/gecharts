#!/usr/bin/python

import sys, glob, subprocess
from nvd3 import pieChart, discreteBarChart, multiBarHorizontalChart

path = sys.argv[1]
# files = glob.glob(path +"*")
# print(files)

out = subprocess.Popen("ls -t %s*" % path, shell=True, stdout=subprocess.PIPE).stdout.readlines()

get_apis = {}
post_apis = {}
delete_apis = {}
patch_apis = {}


def write_files(file, info, scripts):
    f = open("./%s" % file, "w")
    f.write(scripts)
    f.write(info)
    f.close()

def generate_chart(data, file, type=None):
    if not type:
        type = 'multiBarHorizontalChart'

    xdata, ydata = [], []
    html = """
        <link href="/home/chcao/cc-dev/gechart/static/nvd3/build/nv.d3.css" rel="stylesheet" type="text/css">
        <script src="/home/chcao/cc-dev/gechart/static/d3/d3.js"></script>
        <script src="/home/chcao/cc-dev/gechart/static/d3/d3.min.js"></script>
        <script src="/home/chcao/cc-dev/gechart/static/nvd3/build/nv.d3.js"></script>
        """
    for k, v in data.iteritems():
        xdata.append(k)
        ydata.append(v)

    # piechart
    chart = pieChart(name=type, color_category='category20c', height=900, width=1500)
    extra_serie = {"tooltip": {"y_start": "Number: ", "y_end": ""}}
    chart.add_serie(y=ydata, x=xdata, extra=extra_serie)
    chart.buildcontent()
    write_files(file, chart.htmlcontent, html)

    # Bar charts
    # chart = discreteBarChart(name=type, height=900, width=1400)
    # chart.add_serie(y=ydata, x=xdata)
    # chart.buildhtml()
    # write_files(file, chart.htmlcontent, html)

    # multiBarHorizontalChart
    # chart = multiBarHorizontalChart(name=type, height=900, width=1400, tooltips=True)
    # chart.add_serie(y=ydata, x=xdata)
    # chart.buildcontent()
    # write_files(file, chart.htmlcontent, html)


ips = []
for f in out:
    lines = open(f.strip()).readlines()
    for l in lines:
        if "rest_api/v1" in l:
            ip = l.split("-")[0].strip()
            if ip not in ips:
                ips.append(ip)
            api = l.split("rest_api/v1")[1].split("/")
            if api[1]:
                re_api = api[1]
            else:
                re_api = api[2]
            if "?" in re_api:
                re_api = re_api.split("?")[0]

            # print re_api
            re_api = re_api.split(" ")[0]

            endpoint = "/rest_api/v1/" + re_api
            if endpoint == '/rest_api/v1/"':
                continue

            if "GET" in l:
                if get_apis.has_key(endpoint):
                    get_apis[endpoint] += 1
                else:
                    get_apis[endpoint] = 1
            elif "POST" in l:
                if post_apis.has_key(endpoint):
                    post_apis[endpoint] += 1
                else:
                    post_apis[endpoint] = 1
            elif "PATCH" in l:
                if patch_apis.has_key(endpoint):
                    patch_apis[endpoint] += 1
                else:
                    patch_apis[endpoint] = 1
            else:
                if delete_apis.has_key(endpoint):
                    delete_apis[endpoint] += 1
                else:
                    delete_apis[endpoint] = 1

# def print_apis(api):
#     for k, v in api.iteritems():
#         print("The endpoint is => %s, total visit number is => %s" %(k, v))
# print(len(set(ips)))
# print("DELETE Requests:")
# print_apis(delete_apis)
# print("\nPATCH Requests:")
# print_apis(patch_apis)
# print("\nGET Requests:")
# print_apis(get_apis)
# print("\nPOST Requests:")
# print_apis(post_apis)
# generate_chart(delete_apis, "delete_api.html")
# generate_chart(patch_apis, "patch_api.html")
generate_chart(get_apis, "get_pie_api.html")
# generate_chart(post_apis, "post_pie_api.html")
