from django.shortcuts import render

from django.views import generic

from .models import BulkArticle, Customer, Equipment, Handover, Workplace

from .forms import HandoverForm

from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.contenttypes.models import ContentType

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from itertools import chain

@method_decorator(login_required, name='dispatch')
class EquipmentListView(generic.ListView):
    def get_queryset(self):
        return list(chain(Equipment.objects.all(), BulkArticle.objects.all()))
    template_name = 'inventory/listEquipment.html'

@method_decorator(login_required, name='dispatch')
class EquipmentDetailsView(generic.DetailView):
    model = Equipment
    template_name = 'inventory/detailEquipment.html'

@method_decorator(login_required, name='dispatch')
class WorkplaceListView(generic.ListView):
    model = Workplace
    template_name = 'inventory/listWorkplace.html'

@method_decorator(login_required, name='dispatch')
class WorkplaceDetailsView(generic.DetailView):
    model = Workplace

    def get_object(self, queryset=None):
        obj = super(WorkplaceDetailsView, self).get_object(queryset=queryset)
        obj.handovers = Handover.objects.filter(
            user_object_id=obj.pk, 
            user_content_type=ContentType.objects.get_for_model(obj))
        return obj
    template_name = 'inventory/detailWorkplace.html'
    
@method_decorator(login_required, name='dispatch')
class CustomerListView(generic.ListView):
    model = Customer
    template_name = 'inventory/listCustomer.html'
    

@login_required
def createHandover(request, objType, pk):
    
    if request.method == 'POST':
        
        form = HandoverForm(request.POST)
        if form.is_valid():

            equipment = None
            if objType == "equipment":
                equipment = Equipment.objects.get(id=pk)
            else:
                equipment = BulkArticle.objects.get(id=pk)
            
            newHandover = Handover()

            newHandover.thing_content_type = ContentType.objects.get_for_model(equipment)
            newHandover.thing_object_id = pk

            workplace = form.cleaned_data['workplace']
            customer = form.cleaned_data['customer']

            recipient = None

            if workplace == None and customer != None:
                recipient = customer
            elif workplace != None and customer == None:
                recipient = workplace

            if recipient != None:
                newHandover.user_object_id = recipient.id
                newHandover.user_content_type =  ContentType.objects.get_for_model(recipient)
                newHandover.movementType = Handover.MovementType.LAY
                newHandover.save()

                return HttpResponseRedirect('/inventory/listEquipment/')

    else:
        form = HandoverForm()

    return render(request, 'inventory/createHandover.html', {'form': form, 'objType':objType, 'pk': pk})

@login_required
def giveBack(request, handoverID):
    
    handoverObj = Handover.objects.get(id=handoverID)

    user = handoverObj.getUser()
    thing = handoverObj.getThing()

    if request.method == 'POST':
        newHandover = Handover()

        newHandover.thing_content_type = ContentType.objects.get_for_model(thing)
        newHandover.thing_object_id = thing.id
        newHandover.user_object_id = user.id
        newHandover.user_content_type =  ContentType.objects.get_for_model(user)
        newHandover.movementType = Handover.MovementType.LAYBACK
        newHandover.save()

        return HttpResponseRedirect('/inventory/detailWorkplace/' + str(user.id))

    return render(request, 'inventory/giveBack.html', { 'user':user, 'thing':thing })
