from django.shortcuts import render

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import ContactForm
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import redirect
from django.utils.html import strip_tags
from urllib.parse import unquote

import firebase_admin
from firebase_admin import credentials, db

# Tensorflow IA
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError
from django.conf import settings

import tensorflow as tf
import numpy as np


from django.shortcuts import render
import os

# emails
import string
import json

from django.contrib.auth import get_user_model
from monitoreoia.models import CustomUser

# Create your views here.


url = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "static/config/firebasekey.json")
cred = credentials.Certificate(url)
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://radiacion-c50d8.firebaseio.com"
})


class minitoringLogin:
    def login(self, request):
        if request.method == 'POST':

            self.username = request.POST.get('username')

            self.password = request.POST.get('password')

            user = authenticate(
                request, username=self.username.lower(), password=self.password)

            context = {'contenido': self.username.lower()}
            if user is not None:
                login(request, user)
                request.session['minitoring_username'] = self.username.lower()
                return render(request, 'home.html', context)
            else:
                # messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
                messages.warning(
                    request, 'Incorrect password or user name, please check! ')
                return render(request, 'alert_nofile.html')

        return render(request, 'login.html')

    def contac(self, request):
        if request.method == 'POST':
            # form = ContactForm(request.POST)

            name = request.POST['name']
            email = request.POST['email']
            subject = request.POST['subject']
            message = request.POST['message']

            # Crear un objeto MIMEText con el mensaje y el tipo de contenido
            # Send the email
            subject = 'GEM platform support - ' + subject
            from_email = 'alruba40@gmail.com'
            to_email = [email, 'arualesb.1@cern.ch']

            message_with_sender = f"Hello {string.capwords(name)}: \n\n \
                        Thank you very much for contacting us!!. \n\n \
                        We will be contacting you shortly by email {email}  to resolve the concern \n\n \
                        \"{message}\" \n\n Best regards \n Alexis Ruales!!"

            # Send the email
            send_mail(subject, message_with_sender, from_email, to_email)

            messages.success(request, f'We will process the request with the email {email.upper()}, \n\n \
                                    ¿Is that correct?')
            return render(request, "confirmation_send_email.html")

        else:
            return render(request, "contact.html")


class Home:
    def home(self, request):
        return render(request, "home.html")

    def contactin(self, request):
        if request.method == 'POST':
            # form = ContactForm(request.POST)

            name = request.POST['name']
            email = request.POST['email']
            subject = request.POST['subject']
            message = request.POST['message']

            # Crear un objeto MIMEText con el mensaje y el tipo de contenido
            # Send the email
            subject = 'GEM platform support - ' + subject
            from_email = 'alruba40@gmail.com'
            to_email = [email, 'arualesb.1@cern.ch']

            message_with_sender = f"Hello {string.capwords(name)}: \n\n \
                        Thank you very much for contacting us!!. \n\n \
                        We will be contacting you shortly by email {email}  to resolve the concern \n\n \
                        \"{message}\" \n\n Best regards \n Alexis Ruales!!"

            # Send the email
            send_mail(subject, message_with_sender, from_email, to_email)

            messages.success(request, f'We will process the request with the email {email.upper()}, \n\n \
                                    ¿Is that correct?')
            return render(request, "confirmation_send_emailin.html")
        else:
            return render(request, "contactin.html")


class database:
    def search_view(self, request):
        # Datbase

        ref = db.reference('database')

        # name user
        minitoring_username = request.session.get('minitoring_username')

        if minitoring_username:
            User = get_user_model()
            options = list(["None"])
            try:
                user = CustomUser.objects.get(username=minitoring_username)
                user_id_to_delete = user.id

                data = ref.child(str(user_id_to_delete)).get()
                try:
                    options = list(data.keys())
                except:
                    options = list(["None"])

                data_points = []
                selected_option = ""
                data_vale = []
                if request.method == 'POST':

                    try:
                        selected_option = request.POST.get('selected_option')
                        datal = data[selected_option]
                        primer_elemento = next(iter(datal.items()))
                        clave, valor = primer_elemento

                        data_vale = [int(number)
                                     for number in valor.split(",")]
                        for i in range(len(data_vale)):
                            data_points.append({"x": i+1, "y": data_vale[i]})
                    except:
                        data_points = [{"x": 0, "y": 0}]
                        pass

                else:

                    try:
                        selected_option = options[0]
                        datal = data[selected_option]
                        primer_elemento = next(iter(datal.items()))
                        clave, valor = primer_elemento

                        data_vale = [int(number)
                                     for number in valor.split(",")]
                        for i in range(len(data_vale)):
                            data_points.append({"x": i+1, "y": data_vale[i]})
                    except:
                        data_points = [{"x": 0, "y": 0}]
                        pass

            except User.DoesNotExist:
                print("User with the specified email does not exist.")

            return render(request, 'search_espectral.html', {'options': options,
                                                             'selected_option': selected_option,
                                                             'data': data_points,
                                                             'dataspectral': data_vale,
                                                             'selectoption': [selected_option]})
        else:
            messages.success(
                request, f'Please enter the username and password again!')
            return render(request, "uploadloging.html")

class realtimeconect:
    def realtimeview(self, request):
        firebase_database_url = "https://radiacion-c50d8.firebaseio.com"  # Coloca la URL correcta aquí
        
        return render(request, "raltimeconection.html", {"firebase_database_url": firebase_database_url})
        """print("aqui estoy en real")


        # Referencia a la ubicación de datos en tiempo real
        refdata = db.reference('edison')  # Reemplaza con la ubicación real de tus datos

    

        # Función de manejo de cambios
        datosrt=""
        data_points = []
        def handle_change(event):
            nonlocal data_points          
        
            datosrt = str(event.data.get('datos', '')).replace(" ", "")
           # print(datosrt)
            if datosrt.endswith(","):
                new_data= datosrt[:-1]
            else:
                new_data = datosrt
            
            data_vale = [int(number) for number in new_data.split(",")]
            
            data_points  = [{"x": i + 1, "y": data_vale[i]} for i in range(len(data_vale))]
            #print("Después de la manipulación:", data_points)
            return render(request, "raltimeconection.html", {'datalive': data_points})


        a=refdata.listen(handle_change)
        
        print("data_point: ",a)
        
        return render(request, "raltimeconection.html", {'datalive': data_points})"""



class CustomFileSystemStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        self.delete(name)
        return name


class iaMossbauer:
    def modelIa(self, request):

        message = ""
        prediction = ""
        fss = CustomFileSystemStorage()
        try:
            # Load Model
            model = tf.keras.models.load_model(
                os.getcwd() + os.path.join(os.sep, "model", "Mossbauer_model.h5")
            )

            spectrum = request.FILES["file"]
            print("Name", spectrum.file)
            _spectrum = fss.save(spectrum.name, spectrum)
            path = str(settings.MEDIA_ROOT) + "/" + spectrum.name
            # read the spectrum
            spec_ = -np.loadtxt(path, dtype=float)[:, 1] / 10
            spec_ = spec_.tolist()

            spectrum_pred = [spec_]
            categ = ["Otro", "Hematita", "Magnetita"]
            result = np.argmax(model.predict(spectrum_pred), axis=-1)

            print("Prediction: " + str(np.argmax(result)))

            prediction = categ[result[0]]

            return render(request, 'iamossbauer.html', {
                "message": message,
                "spectrum": spectrum_pred,
                "prediction": prediction
            })

        except MultiValueDictKeyError:
            return render(request, 'iamossbauer.html', {
                "message": "No File Selected"
            })


class iaMossbauerRT:
    def modelIaRT(self, request):

        message = ""
        prediction = ""
        fss = CustomFileSystemStorage()
        try:
            # Load Model
            model = tf.keras.models.load_model(
                os.getcwd() + os.path.join(os.sep, "model", "Mossbauer_model.h5")
            )

            spectrum = request.FILES["file"]
            print("Name", spectrum.file)
            _spectrum = fss.save(spectrum.name, spectrum)
            path = str(settings.MEDIA_ROOT) + "/" + spectrum.name
            # read the spectrum
            spec_ = -np.loadtxt(path, dtype=float, delimiter=',')
            spec_ = spec_.T
            spec_ = (spec_ - spec_.mean())/(spec_.std())
            spec_ = spec_.tolist()

            spectrum_pred = [spec_]
            categ = ["Otro", "Hematita", "Magnetita"]
            result = np.argmax(model.predict(spectrum_pred), axis=-1)

            print("Prediction: " + str(np.argmax(result)))

            prediction = categ[result[0]]

            return render(request, 'iamossbauer_realtime.html', {
                "message": message,
                "spectrum": spectrum_pred,
                "prediction": prediction
            })

        except MultiValueDictKeyError:
            return render(request, 'iamossbauer_realtime.html', {
                "message": "No File Selected"
            })


class iaMossbauerRTL:
    def modelIaRTL(self, request):
        # Datbase
        print("aqui estoy")
        ref = db.reference('database')

        # model
        message = ""
        prediction = ""

        # name user
        minitoring_username = request.session.get('minitoring_username')

        if minitoring_username:
            User = get_user_model()
            options = list(["None"])
            try:
                user = CustomUser.objects.get(username=minitoring_username)
                user_id_to_delete = user.id

                data = ref.child(str(user_id_to_delete)).get()
                try:
                    options = list(data.keys())
                except:
                    options = list(["None"])

                data_points = []
                selected_option = ""
                data_vale = []

                # Load Model
                model = tf.keras.models.load_model(
                    os.getcwd() + os.path.join(os.sep, "model", "Mossbauer_model.h5")
                )

                if request.method == 'POST':

                    try:
                        selected_option = request.POST.get(
                            'selected_option')
                        datal = data[selected_option]
                        primer_elemento = next(iter(datal.items()))
                        clave, valor = primer_elemento

                        

                        data_vale = [int(number)
                                     for number in valor.split(",")]
                        
                        print(len(data_vale))

                        spec_ = -np.array(data_vale)
                        spec_ = spec_.T
                        spec_ = (spec_ - spec_.mean())/(spec_.std())
                        spec_ = spec_.tolist()

                        spectrum_pred = [spec_]
                        categ = ["Otro", "Hematita", "Magnetita"]
                        result = np.argmax(
                            model.predict(spectrum_pred), axis=-1)

                        print("Prediction: " + str(np.argmax(result)))

                        prediction = categ[result[0]]

                        for i in range(len(data_vale)):
                            data_points.append({"x": i+1, "y": data_vale[i]})
                    except:
                        data_points = [{"x": 0, "y": 0}]
                        pass

                else:

                    try:
                        selected_option = options[0]
                        datal = data[selected_option]
                        primer_elemento = next(iter(datal.items()))
                        clave, valor = primer_elemento

                        data_vale = [int(number)
                                     for number in valor.split(",")]
                        
                        print(len(data_vale))

                        spec_ = -np.array(data_vale)
                        spec_ = spec_.T
                        spec_ = (spec_ - spec_.mean())/(spec_.std())
                        spec_ = spec_.tolist()

                        spectrum_pred = [spec_]
                        categ = ["Otro", "Hematita", "Magnetita"]
                        result = np.argmax(
                            model.predict(spectrum_pred), axis=-1)

                        print("Prediction: " + str(np.argmax(result)))

                        prediction = categ[result[0]]


                        for i in range(len(data_vale)):
                            data_points.append({"x": i+1, "y": data_vale[i]})
                    except:
                        data_points = [{"x": 0, "y": 0}]
                        pass

            except User.DoesNotExist:
                print("User with the specified email does not exist.")

            return render(request, 'iamossbauer_realtimeL.html', {'options': options,
                                                                  'selected_option': selected_option,
                                                                  'data': data_points,
                                                                  "prediction": prediction,
                                                                  'dataspectral': data_vale,
                                                                  'selectoption': [selected_option]})
        else:
            messages.success(
                request, f'Please enter the username and password again!')
            return render(request, "uploadloging.html")
