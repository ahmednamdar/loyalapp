import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from core.models import Order, customer
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.core.serializers import serialize
from django.core import serializers

# Create your views here.


def index(request):

    return HttpResponse('<h1></h1> ')


def index2(request):

    return HttpResponse('<h1>Welcome to loyal app</h1>')


def print_id(request, id):

    custom = customer.objects.get(identity=id)
    return render(request, 'print.html', {'custom': custom})


def my_pdf_view(request, id):
    custom = customer.objects.get(identity=id)
    template = get_template('print.html')
    html = template.render({'custom': custom})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="print.pdf"'
    result = BytesIO()
    pisa_status = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pisa_status.err:
        return HttpResponse(result.getvalue(), 'application/pdf')
    return response


def send(requet, phone):
    return


def analytics(request):
    orders = Order.objects.all()
    myObjs = []
    for x in orders:
        dic = {}
        dic['name'] = x.customer.first_name + ' ' + x.customer.last_name
        dic['id'] = x.customer.identity.__str__()
        dic['table'] = x.tableNumber
        dic['date'] = x.date.__str__()
        dic['total'] = x.totalPrice.__str__()
        myObjs.append(dic)

    data = json.dumps(myObjs)
    # data = serialize('json',orders, use_natural_primary_keys=True, use_natural_foreign_keys=True)
    # return HttpResponse(data,content_type='application/json')
    return render(request, 'analytics.html', {'orders': data})


def getOrders(request):
    orders = Order.objects.all()
    myObjs = []
    for x in orders:
        dic = {}
        dic['name'] = x.customer.first_name + ' ' + x.customer.last_name
        dic['id'] = x.customer.identity.__str__()
        dic['table'] = x.invoice.tableNumber
        dic['date'] = x.date_placed.__str__()
        dic['total'] = x.invoice.totalPrice.__str__()
        myObjs.append(dic)

    data = json.dumps(myObjs)
    # data = serializers.serialize('json',orders, use_natural_primary_keys=True, use_natural_foreign_keys=True)
    return JsonResponse(data, safe=False)


def history(request, id):
    intID = int(id)
    result = customer.objects.get(identity=intID)
    orders = Order.objects.filter(customer=result).order_by('-date')
    print(result)
    context = {'orders': orders}
    return render(request, 'history.html', context)
    # return HttpResponse("<h1>gg</h1>")
