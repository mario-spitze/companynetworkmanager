from django.shortcuts import render

from django.views import generic

from .models import BulkArticle, Equipment, Handover, Workplace

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

@login_required
def createHandover(request, pk):
    
    if request.method == 'POST':
        
        form = HandoverForm(request.POST)
        if form.is_valid():

            equipment = Equipment.objects.get(id=pk)
            newHandover = Handover()
            newHandover.thing_content_type = ContentType.objects.get_for_model(equipment)
            newHandover.thing_object_id = pk

            workplace = form.cleaned_data['workplace']
#            workplace = Workplace.objects.get(workplaceId)
            newHandover.user_object_id = workplace.id
            newHandover.user_content_type =  ContentType.objects.get_for_model(workplace)

            newHandover.save()

            return HttpResponseRedirect('/inventory/listEquipment/')

    else:
        form = HandoverForm()

    return render(request, 'inventory/setHandover.html', {'form': form, 'pk': pk})