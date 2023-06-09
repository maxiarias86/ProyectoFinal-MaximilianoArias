from django.shortcuts import render,redirect
from .models import *
from .forms import *
from AppUsuarios.models import *
from AppUsuarios.views import *
from AppUsuarios.forms import *
from django.http import HttpResponse

# Create your views here.

def verCuento(request, id):
    
    cuento=Cuento.objects.get(id=id)
    categoria=cuento.categoria
    titulo=cuento.titulo
    subtitulo=cuento.subtitulo
    cuerpo=cuento.cuerpo
    autor=cuento.autor
    fecha=cuento.fecha
    foto=cuento.foto.url
    id=cuento.id
    
    return render(request, 'AppCuentos/verCuento.html', {'id':id, 'categoria':categoria,'titulo':titulo,'subtitulo':subtitulo,'cuerpo':cuerpo,'autor':autor,'fecha':fecha,'foto':foto,"avatar":obtenerAvatar(request)})

@login_required
def nuevoCuento(request):
    
    if request.method =='POST':
        form=CuentoForm(request.POST,request.FILES)
        if form.is_valid():
            info=form.cleaned_data
            
            cuento=Cuento()
            cuento.fecha=datetime.date.today()
            cuento.categoria=info['categoria']
            cuento.autor=request.user
            cuento.titulo=info["titulo"]
            cuento.subtitulo=info['subtitulo']
            cuento.cuerpo=info['cuerpo']
            cuento.foto=request.FILES["foto"]

            palabras=cuento.cuerpo.split()
            if len(palabras)>1000:
                mensaje="Lamentablemente el cuento tiene más de mil palabras, no ha sido cargado"
            else:
                cuento.save()
                mensaje="Felicitaciones es el autor de un cuento nuevo"


            return render(request,"AppCuentos/inicioCuentos.html", {"mensaje":mensaje,"avatar":obtenerAvatar(request)})
        else:
            return render(request,"AppCuentos/inicioCuentos.html", {"mensaje":'Error al agregar el cuento',"avatar":obtenerAvatar(request)})
         
    else:
        form=CuentoForm()
        return render(request, "AppCuentos/nuevoCuento.html", {"form": form,"avatar":obtenerAvatar(request)})   

def inicioCuentos(request):
    cuentos=Cuento.objects.all()
    if len(cuentos)==0:
        mensaje="Aún no hay cuentos cargados... Inspirate y da el primer paso"
    else:
        mensaje=''
    return render(request,"AppCuentos/inicioCuentos.html", {'cuentos':cuentos,'mensaje':mensaje,"avatar":obtenerAvatar(request)})

def buscarCuento(request):
    titulo=request.GET['titulo']
    if titulo!='':
        cuentos=Cuento.objects.filter(titulo__icontains=titulo)
        if len(cuentos)==0:
                mensaje='No existen cuentos con ese título'
        else:
            mensaje=''
        return render(request, 'AppCuentos/inicioCuentos.html',{'mensaje':mensaje,'cuentos':cuentos,"avatar":obtenerAvatar(request)})
    else:
        return render(request, 'AppCuentos/inicioCuentos.html',{'mensaje':'Ingrese una palabra clave a buscar',"avatar":obtenerAvatar(request)})

@login_required
def mensajeAlAutor(request, id):
    cuento=Cuento.objects.get(id=id)
    if request.method =='POST':
        form=MensajeAlAutorForm(request.POST)
        
        if form.is_valid():
            info=form.cleaned_data
            
            mensaje=Mensaje()
            mensaje.remitente=request.user
            mensaje.titulo=info["titulo"]
            mensaje.destinatario=cuento.autor
            mensaje.contenido=info["contenido"]
            mensaje.fecha=datetime.date.today()
            
            mensaje.save()
            
            return render(request,"AppUsuarios/inicioUsuarios.html", {"mensaje":'Mensaje enviado con éxito',"avatar":obtenerAvatar(request)})
    else:
        form=MensajeAlAutorForm()
        return render(request, "AppCuentos/mensajeAlAutor.html", {"form": form,"avatar":obtenerAvatar(request)})

@login_required
def eliminarCuento(request, id):
    cuento = Cuento.objects.get(id=id)
    cuento.delete()

    return render(request, "AppCuentos/inicioCuentos.html", {'mensaje':f'Cuento "{cuento.titulo}" eliminado ',"avatar":obtenerAvatar(request)})

@login_required
def misCuentos(request):
    cuentos=Cuento.objects.all()
    if len(cuentos)==0:
        mensaje="Aún no hay cuentos cargados... Inspirate y da el primer paso"
    else:
        mensaje=''
    return render(request,"AppCuentos/misCuentos.html", {'cuentos':cuentos,'mensaje':mensaje,"avatar":obtenerAvatar(request)})

def buscarPorCategoria(request):
    if request.method == 'POST':
        categoria=request.POST['categoria']
        cuentos=Cuento.objects.filter(categoria__icontains=categoria)
        if len(cuentos)==0:
                mensaje=f'Aún no hay cuentos de {categoria}, inspírate y carga el primero'
        else:
            mensaje=''

        return render (request, 'AppCuentos/inicioCuentos.html', {'mensaje':mensaje,'cuentos':cuentos,"avatar":obtenerAvatar(request)})
    else:
        form=buscarPorCategoriaForm()
        return render (request, 'AppCuentos/buscarPorCategoria.html', {'form':form,"avatar":obtenerAvatar(request)})

def editarCuento(request, id):
    cuentoViejo=Cuento.objects.get(id=id)
    print(cuentoViejo)
    
    if request.method == 'POST':
        form=EditarCuentoForm(request.POST, request.FILES)
        
        if form.is_valid():
            
            info=form.cleaned_data
            
            cuentoEditado=Cuento()
            cuentoEditado.fecha=datetime.date.today()
            cuentoEditado.categoria=info['categoria']
            cuentoEditado.autor=cuentoViejo.autor
            cuentoEditado.titulo=cuentoViejo.titulo
            cuentoEditado.subtitulo=info['subtitulo']
            cuentoEditado.cuerpo=info['cuerpo']
            cuentoEditado.foto=request.FILES["foto"]

            palabras=cuentoEditado.cuerpo.split()
            if len(palabras)>1000:
                mensaje="Lamentablemente el cuento tiene más de mil palabras, no ha sido editado"
            else:
                cuentoViejo.delete()
                
                cuentoEditado.save()
                mensaje="El cuento ha sido modificado"


            return render(request,"AppCuentos/inicioCuentos.html", {"mensaje":mensaje,"avatar":obtenerAvatar(request)})
        else:
            return render(request,"AppCuentos/inicioCuentos.html", {"mensaje":'Error al editar el cuento',"avatar":obtenerAvatar(request)})
         
    else:
        form=EditarCuentoForm()
        return render(request, "AppCuentos/editarCuento.html", {"mensaje":f'Editando {cuentoViejo.titulo}',"form": form,"avatar":obtenerAvatar(request)})