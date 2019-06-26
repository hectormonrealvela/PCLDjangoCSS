from django.shortcuts import get_object_or_404
from django.http import *
import numpy as np
from open3d import read_point_cloud
from plotly.offline import plot
import plotly.graph_objs as go
from django.shortcuts import redirect, render
from django.views.generic import View , ListView
from django.contrib.auth import authenticate, login, logout
from . forms import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import re











# **************************************************************************** LOGIN / REGISTRO ***************************************************************#

def logout_view(request):#Función para desloguearte
    logout(request)
    return redirect('../../')


class LoginFormView(View): #Vista que se encarga del login del usuario.
    form_class = LoginForm
    template_name = 'Document/login.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('../list')

        return render(request, self.template_name, {'form': form})


class RegisterFormView(View): # vista que se encarga del nuevo registro de un usuario
    form_class = RegisterForm
    template_name = 'Document/register.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})


    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            if user is not None:

                if user.is_active:
                    login(request, user)
                    return redirect('../')

        return render(request, self.template_name, {'form': form})





#********************************************************************** LISTAS ************************************************************************************#



class list(ListView):

    model = Document
    template_name = 'Document/list.html'
    paginate_by = 8
    context_object_name="object_list"

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            object_list = self.model.objects.filter(numb__icontains=query).filter(user=self.request.user).order_by('numb')
            return object_list
        else:
            return Document.objects.filter(user=self.request.user).order_by('numb')



class borrar(ListView):
    model = Document
    template_name = 'Document/borrar.html'
    paginate_by = 8
    context_object_name = "object_list"


    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            object_list = self.model.objects.filter(numb__icontains=query).filter(user=self.request.user).order_by('numb')
            return object_list
        else:
            return Document.objects.filter(user=self.request.user).order_by('numb')


class grafica(ListView): # Lista en la que pdoremos seleccionar que gráfica queremos representar
    model = Document
    template_name = 'Document/grafica.html'
    paginate_by = 8
    context_object_name = "object_list"

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            object_list = self.model.objects.filter(numb__icontains=query).filter(user=self.request.user).order_by('numb')
            return object_list
        else:
            return Document.objects.filter(user=self.request.user).order_by('numb')








#******************************************************************************** SUBIR ARCHIVOS *************************************************************************************#



def simple_upload(request): #Con esta función definimos cómo subir varios Documentos
        user=request.user
        if request.method == "POST":
            files = request.FILES.getlist('myfiles')

            for number, file in enumerate(files): #
                value = str(file) #Pasamos el nombre de cada fichero que queremos subir a la variable
                value= re.sub("\D", "", value) #Remueve todo del string excepto los digitos
                instance = Document( #Guardamos el nombre del documento, el numero del usuario y el de cada fichero que hemos subido en la base de datos
                    document = file,
                    Nombre = file,
                    user = user,
                    numb = value
                )

                if Document.objects.filter(Nombre = instance.Nombre).filter(user=request.user).exists():

                    print("¡Este documento ya existe!")
                    pass

                else:
                    instance.save()
            request.session['number_of_files'] = number + 1
            return redirect('../list')

        return render(request, 'Document/simple_upload.html')






#*****************************************************************************************  BORRAR ARCHIVOS ******************************************************************************************#



def delete_view(request, id): # borramos el documento que hayamos escogido anteriormente

        obj = get_object_or_404(Document, id=id)
        if request.method == "POST":
            obj.delete()
            return redirect('borrar')
        context = {
            "object": obj
        }
        return render(request, "Document/delete.html", context)







#****************************************************************************************** CREAR PCL ***********************************************************#


def create_image(request, numb): # Representación Nube de puntos.

    document = Document.objects.filter(user=request.user).get(numb=numb)
    filename = document.document.path
    nombre = document.Nombre

    pcd = read_point_cloud(filename)
    pcd_array = (np.asarray(pcd.points))

    x = []
    y = []
    z = []

    for row in pcd_array:
        x.append(float(row[0]))
        y.append(float(row[1]))
        z.append(float(row[2]))

    trace1 = go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode='markers',
        marker=dict(
            size=0.75,
            color=z,
            colorscale='Earth',
            symbol='circle',
        ),

    )

    data = [trace1]
    layout = go.Layout(
        scene=dict(
            xaxis=dict(
                range=[-100, 100], ),
            yaxis=dict(
                range=[-100, 100], ),
            zaxis=dict(
                range=[-100, 100], ), ),
        width=1000,
        height=700, showlegend=False)

    fig = go.Figure(data=data, layout=layout, )
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)

    context = {
        "plot": plot_div,
        "filename": nombre,
        "Document": document,

    }

    return render(request, 'Document/plot.html',context)



def prueba(request):
    return render(request, 'Document/prueba.html')

