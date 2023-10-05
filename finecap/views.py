from django.shortcuts import render,get_object_or_404,redirect
from .models import Reserva, Stand
from .forms import ReservaForm
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required 

# Create your views here.
@login_required 
def editar(request, id):
    reserva = get_object_or_404(Reserva,id=id)
   
    if request.method == 'POST':
        form = ReservaForm(request.POST, request.FILES,instance=reserva)

        if form.is_valid():            
            form.save()
            return redirect('listar')

    else:
        form = ReservaForm(instance=reserva)

    return render(request,'finecap/form.html',{'form':form})

@login_required
def remover(request, id):
    reserva = get_object_or_404(Reserva, id=id)
    reserva.delete()
    return redirect('listar') # procure um url com o nome 'lista_aluno'

@login_required
def criar(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reserva realizada com sucesso!')
            form = ReservaForm()
    else:
        form = ReservaForm()

    return render(request, "finecap/form.html", {'form': form})

@login_required
def listar(request):
    reserva = Reserva.objects.all().order_by('-data_reserva')
    nome = request.GET.get('nome')
    vf = request.GET.get('vf')
    valor = request.GET.get('valor')
    data = request.GET.get('data')
    

    if nome:
         reserva = reserva.filter(nome_empresa__icontains=request.GET.get('nome'))
    if vf == "quitado":
         reserva = reserva.filter(quitado=True)
    elif vf == "pendente":
        reserva = reserva.filter(quitado=False)
    if valor:
        reserva = reserva.filter(stand__valor=request.GET.get('valor'))
    if data:
        reserva = reserva.filter(data_reserva__icontains=request.GET.get('data'))
    

    paginator = Paginator(reserva, 5)  
    page = request.GET.get('page')
    try:
        reserva = paginator.page(page)
    except PageNotAnInteger:
        reserva = paginator.page(1)
    except EmptyPage:
        reserva = paginator.page(paginator.num_pages)

    context = {
        'reserva': reserva
    }

    return render(request, "finecap/lista.html", context)

@login_required
def detalhes(request, id): 
    reserva = get_object_or_404(Reserva, id=id)
    context = {
        'reserva': reserva
    }
    return render(request, "finecap/detalhes.html", context)
