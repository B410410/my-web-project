from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from firstapp.models import ToDo
from firstapp.serializers import ToDoSerializer

def firstapp():
        todos = ToDo.objects.all()

        # 不使用序列化的處理
        #todos = ToDo.objects.all().values('title', 'description', 'imput_time', 'completed')

        serializer = ToDoSerializer(todos, many=True)
        data = {
            'todos': serializer.data 
        }
        print('todos', todos)
        print('serializer', serializer.data)

        return data


class ToDoList(APIView):
    template_name = 'firstapp.html'
    def get(self, request):
        data = firstapp()
        return render(request, self.template_name, data)

    def post(self, request):
        serializer = ToDoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
