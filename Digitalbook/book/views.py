from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Book,Author
from django.http import JsonResponse,HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json,os,csv
import requests
from .serializers import BookSerializer, AuthorSerializer
from .serializers import BookSerializer, BookSerializer
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.db.models import Q



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

    # try:
    #     #尝试解析请求体为JSON
    #     data = json.loads(request.body)
    # except json.JSONDecodeError:
    #     # 如果解析失败，那么请求可能不包含 JSON 数据
    #     return JsonResponse({'error': 'Invalid JSON'}, status=400)

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
        keyword = request.POST.get('p','le')

        #设置Google Book API请求参数
        api_url = 'https://www.googleapis.com/books/v1/volumes'
        api_key = 'AIzaSyDqgEBeHf2IFcgVy2OqW1A8D_NHBMTpFo0'
        max_results = 40
        total_books = 1000

        fieldnames = ['title', 'description', 'published_date', 'author', 'price', 'subject']

        #读取CSV_FILE_PATH环境变量
        CSV_FILE_PATH = os.getenv('CSV_FILE_PATH','/default/path/to/books.csv')
        print(f"CSV_FILE_PATH: {CSV_FILE_PATH}")#打印

        #发送多次请求，每次最多40本
        with open(CSV_FILE_PATH, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            for start_index in range(0,total_books,max_results):
                params = {
                    'q': keyword,
                    'key': api_key,
                    'maxResults': max_results,
                    'startIndex': start_index
                 }

                try:
                    response = requests.get(api_url, params=params)
                    response.raise_for_status()
                    data = response.json()

                    #提取每本书的信息并进行处理
                    for item in data.get('items', []):
                        volume_info = item.get('volumeInfo', {})
                        title = volume_info.get('title')
                        description = volume_info.get('webReaderLink')
                        publish_date = volume_info.get('publishedDate')
                        authors = volume_info.get('authors', [])
                        author = ', '.join(authors) if authors else ''  #多个作者合并为字符串
                        page_count = volume_info.get('pageCount', 0)
                        price = round(float(page_count), 2)  #pageCount 转换为两位小数的 price
                        subject = volume_info.get('id')

                        #数据库中的 Book 对象
                        book_obj, created = Book.objects.update_or_create(
                            title=title,
                            defaults={
                                'description': description,
                                'publish_date': publish_date,
                                'author': author,
                                'price': price,
                                'subject': subject
                            }
                        )

                        #书籍写入csv文件
                        writer.writerow({
                            'title': title,
                            'description': description,
                            'publish_date': publish_date,
                            'author': author,
                            'price': price,
                            'subject': subject
                        })

                except requests.exceptions.RequestException as e:
                    return JsonResponse({'error': f'API request failed: {str(e)}'}, status=500)

            return JsonResponse({'message': 'Books added successfully.', 'csv_file_path': CSV_FILE_PATH}, status=200)

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

#task4-2
@csrf_exempt
def delete_multiple_books(request):
    if request.method == 'POST':
        digit_to_exclude = request.POST.get('digit_to_exclude', None)
        letter_to_exclude = request.POST.get('letter_to_exclude', None)

        if digit_to_exclude is not None:
            # 使用 Q 对象定义查询条件，以便删除符合条件的书籍
            query = Q(unique_identifier__contains=digit_to_exclude)
            # 使用 bulk_delete() 方法执行批量删除
            deleted_count, _ = Book.objects.filter(query).delete()
            #返回成功删除的数量
            return JsonResponse({'message': f'{deleted_count} books deleted successfully.'}, status=200)

        if letter_to_exclude is not None:
            #使用Q对象定义查询条件，以便删除符合条件的书籍
            query = Q(title__icontains=letter_to_exclude)
            #使用bulk_delete() 方法执行批量删除
            deleted_count, _ = Book.objects.filter(query).delete()
            #返回成功删除的数量
            return JsonResponse({'message': f'{deleted_count} books deleted successfully.'}, status=200)

    # 如果请求方法不是 POST，则返回错误响应
    return JsonResponse({'error': 'Invalid request method'}, status=405)