# DigitalbookInventory
Operation of editing Digitalbookstore

Install environment
pip install django
check version of django by python -m django --version
check the list of subcommands by django-admin

python manage.py runser

Build database
python manage.py makemigrations
python manage.py migrate

Use shell
python manage.py shell
quit by exit


#check add_multiple_books function -- use Postman
input http://127.0.0.1:8000/delete_multiple_books/ and select POST
set key-value in body
set digit_to_exclude to match id
set letter_to_exclude to match title
click send and observe status and message
