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
from queryset_sequence import QuerySetSequence

@method_decorator(login_required, name='dispatch')
class HardwareClassCreateView(generic.CreateView):
    model = HardwareClass
    fields = ['name']
    def get_success_url(self) -> str:
        return reverse_lazy('inventory:listHardwareClass')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['operation'] = "create"
        return context

@method_decorator(login_required, name='dispatch')
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

@method_decorator(login_required, name='dispatch')
class EquipmentCreateView(generic.CreateView):
    model = Equipment
    fields = ['base', 'sn', 'inventarNr' ]
    template_name = 'inventory/createEquipment.html'
    def get_success_url(self) -> str:
        return reverse_lazy('inventory:listEquipment')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['operation'] = "create"
        return context

@method_decorator(login_required, name='dispatch')
class EquipmentUpdateView(generic.UpdateView):
    model = Equipment
    fields = ['base', 'sn', 'inventarNr']
    template_name = 'inventory/createEquipment.html'
    success_url = reverse_lazy('inventory:listEquipment')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['operation'] = "update"
        return context

@method_decorator(login_required, name='dispatch')
class EquipmentListView(generic.ListView):
    def get_queryset(self):
#        result = list(chain(Equipment.objects.all(), BulkArticle.objects.all()))
        data = QuerySetSequence(Equipment.objects.all(), BulkArticle.objects.all())
        result = None
        order_text = self.request.GET.get('order')
        if order_text == 'name':
            result = sorted(
                data,
                key=lambda i: (
                    i.base.name if i.getType == "equipment" else i.name
                )
            )     
        elif order_text == 'sn':
            result = sorted(
                data,
                key=lambda i: (getattr(i, 'i.sn', 0))
            )
        elif order_text == 'class':
            result = sorted(
                data,
                key=lambda i: (
                    i.base.hardwareClass.__str__() if i.getType == "equipment" else i.hardwareClass.__str__())
            )
        else:
            result = data
        return result
    template_name = 'inventory/listEquipment.html'

@method_decorator(login_required, name='dispatch')
class EquipmentDetailsView(generic.DetailView):
    model = Equipment
    template_name = 'inventory/detailEquipment.html'

@method_decorator(login_required, name='dispatch')
class BulkArticleUpdateView(generic.UpdateView):
    model = BulkArticle
    fields = ['name', 'ean', 'hardwareClass', 'status']
    template_name = 'inventory/updateArticle.html'
    success_url = reverse_lazy('inventory:listArticle')

@method_decorator(login_required, name='dispatch')
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

            return HttpResponseRedirect('/inventory/listArticle/')

    else:
        form = ArticleCreateForm()

    return render(request, 'inventory/createArticle.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class ArticleListView(generic.ListView):
    def get_queryset(self):
        order_text = self.request.GET.get('order')
        if order_text == 'name':
            return Article.objects.all().order_by('name')
        elif order_text == 'ean':
            return Article.objects.all().order_by('ean')
        elif order_text == 'type':
            return Article.objects.all().order_by('bulkarticle')
        elif order_text == 'status':
            return Article.objects.all().order_by('status')
        elif order_text == 'class':
            return Article.objects.all().order_by('hardwareClass')
        return Article.objects.all()
    template_name = 'inventory/listArticle.html'  

@method_decorator(login_required, name='dispatch')
class WorkplaceCreateView(generic.CreateView):
    model = Workplace
    fields = ['room', 'place', 'customer', 'comment']
    template_name = 'inventory/createWorkplace.html'
    def get_success_url(self) -> str:
        return reverse_lazy('inventory:listWorkplace')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['operation'] = "create"
        return context

@method_decorator(login_required, name='dispatch')
class WorkplaceUpdateView(generic.UpdateView):
    model = Workplace
    fields = ['room', 'place', 'customer', 'comment']
    template_name = 'inventory/createWorkplace.html'
    success_url = reverse_lazy('inventory:listWorkplace')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['operation'] = "update"
        return context

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
        if obj.customer:
            obj.customerHandovers = Handover.objects.filter(
                movementType=Handover.MovementType.LAY,
                oppositeHandover=None,
                user_object_id=obj.customer.pk, 
                user_content_type=ContentType.objects.get_for_model(obj.customer))
        return obj
    template_name = 'inventory/detailWorkplace.html'

@method_decorator(login_required, name='dispatch')
class CustomerCreateView(generic.CreateView):
    model = Customer
    fields = ['name' ]
    template_name = 'inventory/createCustomer.html'
    def get_success_url(self) -> str:
        return reverse_lazy('inventory:listCustomer')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['operation'] = "create"
        return context

@method_decorator(login_required, name='dispatch')
class CustomerUpdateView(generic.UpdateView):
    model = Customer
    fields = ['name']
    template_name = 'inventory/createCustomer.html'
    success_url = reverse_lazy('inventory:listCustomer')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['operation'] = "update"
        return context

@method_decorator(login_required, name='dispatch')
class CustomerDetailsView(generic.DetailView):
    model = Customer
    def get_object(self, queryset=None):
        obj = super(CustomerDetailsView, self).get_object(queryset=queryset)
        obj.handovers = Handover.objects.filter(
            movementType=Handover.MovementType.LAY,
            oppositeHandover=None,
            user_object_id=obj.pk, 
            user_content_type=ContentType.objects.get_for_model(obj))
        return obj
    template_name = 'inventory/detailCustomer.html'
    
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
                newHandover.commend = form.cleaned_data['commend']
                newHandover.save()

                return HttpResponseRedirect('/inventory/listEquipment/')

    else:
        form = HandoverForm()

    return render(request, 'inventory/createHandover.html', {'form': form, 'objType':objType, 'pk': pk})

@login_required
def giveBack(request, handoverID):
    
    oldHandover = Handover.objects.get(id=handoverID)

    place = oldHandover.getPlace()
    thing = oldHandover.getThing()

    if request.method == 'POST':

        newHandover = Handover()

        newHandover.oppositeHandover = oldHandover
        oldHandover.oppositeHandover = newHandover

        newHandover.thing_content_type = ContentType.objects.get_for_model(thing)
        newHandover.thing_object_id = thing.id
        newHandover.user_object_id = place.id
        newHandover.user_content_type =  ContentType.objects.get_for_model(place)
        newHandover.movementType = Handover.MovementType.LAYBACK
        newHandover.save()
        oldHandover.save()
        if newHandover.user_content_type == ContentType.objects.get_for_model(Customer):
            return HttpResponseRedirect('/inventory/detailCustomer/' + str(place.id))
        return HttpResponseRedirect('/inventory/detailWorkplace/' + str(place.id))

    if oldHandover.user_content_type == ContentType.objects.get_for_model(Customer):
        placeType = "customer"
    else:
        placeType = "workplace"

    return render(request, 'inventory/giveBack.html', { 'place':place, 'thing':thing , 'placeType':placeType})
