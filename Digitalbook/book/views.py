from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Book,Author
from django.http import JsonResponse,HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json
from .serializers import BookSerializer, AuthorSerializer
from .serializers import BookSerializer, BookSerializer
from django.views.decorators.http import require_http_methods



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


#task2-1
def search_books(request):
    if request.method == 'GET':
        #该函数接收一个查询字符串
        #然后返回title中包含这个字符串的所有书籍
        query = request.GET.get('query','')
        books = Book.objects.filter(title__icontains=query)
        serializer = BookSerializer(books, many=True)
        return JsonResponse(serializer.data, safe = False)
    else:
        return JsonResponse({"error":"Method not allowed"})

#task2-2
def sort_books(request):
    if request.method == 'GET':
        #默认按照标题排序
        sort_field = request.GET.get('sort_field','title')
        #默认升序
        sort_direction = request.GET.get('sort_direction','ascending')
        if sort_direction == 'descending':
            sort_field = '-' + sort_field
        books = Book.objects.order_by(sort_field)
        serializer = BookSerializer(books,many=True)
        return JsonResponse(serializer.data, safe = False)
    else:
        return JsonResponse({"error":"Method not allowed"})


#task3-1
@csrf_exempt
@require_http_methods(["PUT","GET"])
def update_book(request,pk):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return JsonResponse({'error':'Book not found'}, status=404)

    data = JSONParser().parse(request)
    serializer = BookSerializer(book,data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data)
    return JsonResponse(serializer.errors, status=400)


#task3-2
@csrf_exempt
def delete_book(request):
    if request.method == 'DELETE':
        data = json.loads(request.body)
        try:
            if 'title' in data:
                book = Book.objects.get(title=data['title'])
            elif 'id' in data:
                #Book.objects.filter(id=data['id']).delete()
                book = Book.objects.get(id=data['id'])
            else:
                return JsonResponse({"error":"Invalid book"})
            book.delete()
            return JsonResponse({"message":"Book has been deleted successfully!"})
        except Book.DoesNotExist:
            return JsonResponse({"error":"Method not allowed"})

#task4-1
@csrf_exempt
def add_multiple_books(request):
    if request.method == 'POST':
        #从请求中获取数据
        data = JSONParser().parse(request)
        book_data = data.get('books')
        serializer = BookSerializer(data=book_data,many=True)#告诉序列化器正在处理多个对象
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'books':serializer.data}, status=201)
        return JsonResponse(serializer.errors, status=400)

#task4-2
@csrf_exempt
def delete_multiple_books(request):
    if request.method == 'POST':
        data = request.POST
        #获取书籍标题
        book_titles = data.getlist('titles')
        count = 0
        for title in book_titles:
            serializer = BookSerializer(data={'title':title})
            if serializer.is_valid():
                books_to_delete = Book.objects.filter(title=title)
                delete_count, _ = books_to_delete.delete()
                count += delete_count
            return JsonResponse({'message':f' {count} books have been deleted successfully!'}, status=200)
    else:
        return HttpResponseBadRequest("Method not allowed")