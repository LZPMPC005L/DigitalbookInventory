# import csv
# from django.core.management.base import BaseCommand
# from django.conf import settings#获取BASE_DIR
# from book.models import Book, Author
# import requests
# import  os,json
#
# class Command(BaseCommand):
#     help = 'Request books data to Google Books API and save results in export_books.json'
#
#     def handle(self, *args, **kwargs):
#         #定义google books api相关参数
#         api_key = os.getenv('AIzaSyDqgEBeHf2IFcgVy2OqW1A8D_NHBMTpFo0')
#         if not api_key:
#             self.stderr.write(self.style.ERROR('Google Books API key is not provided.'))
#             return
#         # if api_key:
#         #     print(f"key found: {api_key}")
#         # else:
#         #     print("invalid key.")
#
#         keyword = 'le'
#         max_results = 40 #每次请求最大结果数
#         total_items = 1000
#         num_batches = (total_items + max_results) - 1 // max_results
#
#         output_file = os.path.join(os.path.dirname(__file__), 'export_books.json')
#
#         for batch_index in range(num_batches):
#             start_index = batch_index * max_results
#             params = {
#                 'q': keyword,
#                 'maxResults': max_results,
#                 'startIndex': start_index,
#                 'key': api_key
#             }
#
#             try:
#                 response = requests.get('https://www.googleapis.com/books/v1/volumes', params=params)
#                 response.raise_for_status()
#                 data = response.json().get('items', [])
#
#                 with open(output_file, 'a', encoding='utf-8') as file:
#                     for item in data:
#                         volume_info = item.get('volumeInfo', {})
#                         book_data = {
#                             'title': volume_info.get('title', 'N/A'),
#                             'description': volume_info.get('description', 'N/A'),
#                             'published_date': volume_info.get('publishedDate', 'N/A'),
#                             'author': ', '.join(volume_info.get('authors', ['N/A'])),
#                             'price': self.get_formatted_price(item),
#                             'subject': ', '.join(volume_info.get('categories', ['N/A']))
#                         }
#                         json.dump(book_data, file)
#                         file.write('\n')
#
#                 self.stdout.write(self.style.SUCCESS(f'Successfully appended {max_results} books to {output_file}'))
#
#             except requests.exceptions.RequestException as e:
#                 self.stderr.write(self.style.ERROR(f'Failed to fetch books from Google Books API: {str(e)}'))
#                 break
#
#         self.stdout.write(self.style.SUCCESS(f'All {total_items} books exported successfully to {output_file}'))