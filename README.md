# Django app for Geocoding #

Python: 3.8.5  
Django: 2.2.17  
MapQuest is used to geocode
- - - -  
Steps to get the application running:
* Clone the repo
* Create a python virtual env  
`python -m venv venv_name`
* Activate the virtual env  
`.\venv_name\Scripts\activate`
* Install the requirements  
`pip install -r requirements.txt`
* Define the MapQuest API Key
   - Windows: `SET MAPQUEST_API_KEY=<Secret API Key>`  
   - Linux  : `export MAPQUEST_API_KEY=<Secret API Key>`  
* Start the Django server  
`python manage.py runserver`
* Go to [http://127.0.0.1:8000/geocode/](http://127.0.0.1:8000/geocode/ "geocode app") 
- - - -  
To use the application:  
* Click on **Choose File**, select ***address_file.xlsx*** present in repo and click on **Submit**
* Once the processing is complete at the backend, updated file having latitude and longitude details would be auto-downloaded
- - - -  
### Links ###  
Signup [here](https://developer.mapquest.com/plan_purchase/steps/business_edition/business_edition_free/register "mapquest signup page") to create a MapQuest API Key
