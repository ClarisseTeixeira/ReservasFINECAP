from django.shortcuts import render,get_object_or_404,redirect
from .models import Reserva, Stand
from .forms import ReservaForm
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger 

# Create your views here.

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

def remover(request, id):
    reserva = get_object_or_404(Reserva, id=id)
    reserva.delete()
    return redirect('listar') # procure um url com o nome 'lista_aluno'


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


def listar(request):
    reserva = Reserva.objects.all().order_by('-data_reserva')
    filtro = request.GET.get('filtro')
    if filtro:
        if filtro.lower() == "quitado":
            reserva = reserva.filter(quitado=True)
        elif filtro.lower() == "pendente":
            reserva = reserva.filter(quitado=False)
        else:
            reserva = reserva.filter(
            Q(nome_empresa__icontains=filtro) |
            Q(stand__valor__icontains=filtro) |
            Q(quitado__icontains=filtro) |
            Q(data_reserva__icontains=filtro)
        )
    paginator = Paginator(reserva, 2)  
    page = request.GET.get('page')
    try:
        reserva = paginator.page(page)
    except PageNotAnInteger:
        reserva = paginator.page(1)
    except EmptyPage:
        reserva = paginator.page(paginator.num_pages)

    context = {
        'filtro': filtro,
        'reserva': reserva
    }

    return render(request, "finecap/lista.html", context)


def detalhes(request, id): 
    reserva = get_object_or_404(Reserva, id=id)
    context = {
        'reserva': reserva
    }
    return render(request, "finecap/detalhes.html", context)
