from django.shortcuts import render

from django.views import generic
from .models import Article, BulkArticle, Customer, Equipment, Handover, HardwareClass, Workplace
from .forms import ArticleCreateForm, HandoverForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from itertools import chain
from django.urls import reverse_lazy

class HardwareClassCreateView(generic.CreateView):
    model = HardwareClass
    fields = ['name']
    success_url = reverse_lazy('inventory:listHardwareClass')

class HardwareClassUpdateView(generic.UpdateView):
    model = HardwareClass
    fields = ['name']
    success_url = reverse_lazy('inventory:listHardwareClass')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['operation'] = "update"
        return context

@method_decorator(login_required, name='dispatch')
class HardwareClassListView(generic.ListView):
    model = HardwareClass
    template_name = 'inventory/listHardwareClass.html'


class EquipmentCreateView(generic.CreateView):
    model = Equipment
    fields = ['base', 'sn', 'inventarNr' ]
    template_name = 'inventory/createEquipment.html'
    success_url = reverse_lazy('inventory:listEquipment')

@method_decorator(login_required, name='dispatch')
class EquipmentListView(generic.ListView):
    def get_queryset(self):
        return list(chain(Equipment.objects.all(), BulkArticle.objects.all()))
    template_name = 'inventory/listEquipment.html'

@method_decorator(login_required, name='dispatch')
class EquipmentDetailsView(generic.DetailView):
    model = Equipment
    template_name = 'inventory/detailEquipment.html'

class BulkArticleUpdateView(generic.UpdateView):
    model = BulkArticle
    fields = ['name', 'ean', 'hardwareClass']
    template_name = 'inventory/updateArticle.html'
    success_url = reverse_lazy('inventory:listArticle')

class ArticleUpdateView(generic.UpdateView):
    model = Article
    fields = ['name', 'ean', 'hardwareClass', 'status']
    template_name = 'inventory/updateArticle.html'
    success_url = reverse_lazy('inventory:listArticle')

@login_required
def createArticle(request):
    
    if request.method == 'POST':

        form = ArticleCreateForm(request.POST)
        if form.is_valid():
            type = form.cleaned_data['type']
            name = form.cleaned_data['name']
            ean = form.cleaned_data['ean']
            hardwareClass = form.cleaned_data['hardwareClass']
            newArticle = None
            if(type=="b"):
                newArticle = BulkArticle(name=name, ean=ean, hardwareClass=hardwareClass)
            elif(type=="i"):
                newArticle = Article(name=name, ean=ean, hardwareClass=hardwareClass)

            newArticle.save()

            return HttpResponseRedirect('/inventory/listEquipment/')

    else:
        form = ArticleCreateForm()

    return render(request, 'inventory/createArticle.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class ArticleListView(generic.ListView):
    def get_queryset(self):
        return Article.objects.all()
    template_name = 'inventory/listArticle.html'  

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
            movementType=Handover.MovementType.LAY,
            oppositeHandover=None,
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
    
    oldHandover = Handover.objects.get(id=handoverID)

    user = oldHandover.getUser()
    thing = oldHandover.getThing()

    if request.method == 'POST':

        newHandover = Handover()

        newHandover.oppositeHandover = oldHandover
        oldHandover.oppositeHandover = newHandover

        newHandover.thing_content_type = ContentType.objects.get_for_model(thing)
        newHandover.thing_object_id = thing.id
        newHandover.user_object_id = user.id
        newHandover.user_content_type =  ContentType.objects.get_for_model(user)
        newHandover.movementType = Handover.MovementType.LAYBACK
        newHandover.save()
        oldHandover.save()

        return HttpResponseRedirect('/inventory/detailWorkplace/' + str(user.id))

    return render(request, 'inventory/giveBack.html', { 'user':user, 'thing':thing })
