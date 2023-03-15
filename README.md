
# Django API Project 



## Deployment with Heroku
1. heroku login
2. touch Procfile
3. web: gunicorn ProjectName.wsgi --log-file -
4. runtime.txt and add your python e.g python-2.7.12
5. pip install gunicorn dj-database-url whitenoise psycopg2
6. pip freeze > requirements.txt
7. ROJECT_ROOT   =   os.path.join(os.path.abspath(__file__))
STATIC_ROOT  =   os.path.join(BASEDIR, 'staticfiles')
STATIC_URL = '/static/'

### Extra lookup directories for collectstatic to find static files
STATICFILES_DIRS = (
    os.path.join(BASEDIR, 'static'),
)

###  Add configuration for static files storage using whitenoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

8.add to middleware  MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
  
]
   

9. add to settings import dj_database_url 
prod_db  =  dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(prod_db)
   
10. heroku create appName
11. ALLOWED_HOSTS = ['appName.herokuapp.com']
12. git init
13. heroku git:remote -a appName
14. git add . && git commit -m "Initial commit"
15. git push heroku master
16. (Optional)
heroku config:set     DISABLE_COLLECTSTATIC=1  
Setting DISABLE_COLLECTSTATIC and restarting
    
17. git push heroku main 
18. heroku run python manage.py migrate

### Solve pycopg2 issues
* brew install openssl
* export LDFLAGS="-L/usr/local/opt/openssl/lib"
* export CPPFLAGS="-I/usr/local/opt/openssl/include"
