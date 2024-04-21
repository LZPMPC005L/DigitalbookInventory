from rest_framework import serializers
from rest_framework.response import Response
from .models import Author
from .models import Book

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['user','name']

    #to_representation方法会在序列化Author对象时被调用，它应该返回一个可以被JSON序列化的对象。它返回了Author对象的name字段。
    def to_representation(self, instance):
        return instance.name


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(many=True)
    class Meta:
        model = Book
        fields = ['id','title','description','published_date','author','price','subject']


    #create方法首先创建一个没有author的Book实例。然后，它遍历author_data_list，对于列表中的每个元素，它都尝试获取一个Author实例，并将其添加到book.author中
    def create(self, validated_data):
        author_data_list = validated_data.pop('author')
        book = Book.objects.create(**validated_data)
        for author_data in author_data_list:
            try:
                #检查是否存在具有给定id的作者
                author = Author.objects.get(id=author_data['id'])
                #检查作者名字是否匹配
                if author.name != author_data['name']:
                    return Response({'error':f'Author name does not match with the given id'},status=400)
                book.authors.add(author)
            except Author.DoesNotExist:
                return Response({'error':f'Author with id{author_data["id"]} does not exist'}, status=400)
        book = Book.objects.create(author=author, **validated_data)
        return book

    def get_author(self,obj):
        if obj.author:
            return [author.name for author in obj.author.all()]
        else:
            return 'Noauthor'