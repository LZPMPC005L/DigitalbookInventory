from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Book,Author
from django.http import JsonResponse,HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json
from .serializers import BookSerializer, AuthorSerializer
from .serializers import BookSerializer, BookSerializer



# def home(request):
#
#     context = {
#         'books':list(Book.objects.all())  #获取所有的book对象并转换为字典列表
#     }
#     return JsonResponse(context)  #返回Json响应

#添加一本书
@csrf_exempt
def add_book(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = BookSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = 201)
        return JsonResponse(serializer.errors, status = 400)
    else:
        return JsonResponse({'error':'Invalid request'}, status = 400)


    # #确保这是一个POST请求
    # if request.method == 'POST':
    #     data = json.loads(request.body)
    #     book = Book.objects.create(
    #         title=data['title'],
    #         description=data['description'],
    #         published_date=data['published_date'],
    #         #author=data['author'],
    #         price=data['price'],
    #         subject=data['subject']
    #     )
    #
    #     author = Author.objects.filter(id__in=data['author_ids'])
    #     book.author.set(author)
    #     book.save()
    #     return JsonResponse({"message":"Book has been added successfully!"})
    # elif request.method == 'GET':
    #     #获取所有的Book对象的字段，并转换为字典列表
    #     data = list(Book.objects.values())
    #     return JsonResponse({"books":data}) #返回书籍数据
    # else:
    #     return JsonResponse({"error":"Method not allowed"})


@csrf_exempt
def add_author(request):
    #确保这是一个POST请求
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = AuthorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.dta, status = 201)
        print(serializer.errors)#打印错误信息
        return JsonResponse({'error':'Invalid request'}, status =400)
    else:
        return JsonResponse({'error':'Invalid request'},status=400)


@csrf_exempt
def get_books(request):
    if request.method == 'GET':
        # 获取所有的Book对象
        books = Book.objects.all()
        # # 创建一个列表来保存所有书籍的数据
        serializer = BookSerializer(books, many=True)
        return JsonResponse(serializer.data, safe = False)
    else:
            # 返回一个包含所有书籍数据的JSON响应
            return JsonResponse({"error":"Invalid request method"})


def get_authors(request):
    if request.method == 'GET':
        authors = Author.objects.all()
        authors_list = list(authors.values())
        return JsonResponse(authors_list,safe=False)
    else:
        return JsonResponse({"error":"Invalid request method"})


@csrf_exempt
def add_book(request):
    #确保这是一个POST请求
    if request.method == 'POST':
        data = json.loads(request.body)
        book = Book.objects.create(
            title=data['title'],
            description=data['description'],
            published_date=data['published_date'],
            #author=data['author'],
            price=data['price'],
            subject=data['subject']
        )

        author = Author.objects.filter(id__in=data['author_ids'])
        book.author.set(author)
        book.save()
        return JsonResponse({"message":"Book has been added successfully!"})
    elif request.method == 'GET':
        #获取所有的Book对象的字段，并转换为字典列表
        data = list(Book.objects.values())
        return JsonResponse({"books":data}) #返回书籍数据
    else:
        return JsonResponse({"error":"Method not allowed"})




class BookView(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        print(serializer.data)
        return Response(serializer.data)



@csrf_exempt
def delete_book(request):

    return


@csrf_exempt
def sort_book(request):

    return



