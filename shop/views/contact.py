from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from ..forms import ContactForm
from ..models import UserForm

class Contact(APIView):
    template_name = 'contact.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('shop:login')
        form = ContactForm()
        data = {'form':form}
        return render(request, self.template_name, data)
    
    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            data_j = {'status':'OK', 'msg':'表單已寄送'}
        else:
            errors = form.errors.as_json()
            data_j = {'status':'ERROR', 'msg': errors}

        return Response(data_j)
    
    # def post(self, request, *args, **kwargs):
    #     if request.method == 'POST':
    #         form = ContactForm(request.POST)
    #         if form.is_valid():
    #             name = form.cleaned_data['user_name']
    #             city = form.cleaned_data['user_city']
    #             is_student = form.cleaned_data['user_school']
    #             email = form.cleaned_data['user_email']
    #             message = form.cleaned_data['user_message']

    #         user = UserForm(
    #             name=name,
    #             city=city,
    #             is_student=is_student,
    #             email=email,
    #             message=message
    #         )
    #         user.save()

    #         data_j = {'status':'OK', 'msg':'表單已寄送'}
    #     else:
    #         data_j = {'status':'ERROR', 'msg':'表單寄送失敗'}

    #     return Response(data_j)