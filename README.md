
##This a DjangoProjectDEployed on Heroku
#===========Role==========
CREATE TABLE Roles(
   roleId serial PRIMARY KEY,
   roleName VARCHAR (255) UNIQUE NOT NULL
);
#============Users==============
CREATE TABLE public.users
(
    user_id serial PRIMARY KEY ,
    username  VARCHAR ( 50 ) NOT NULL,
    password  VARCHAR ( 50 ) NOT NULL,
    email  VARCHAR ( 255 )  NULL,
    created_on  TIMESTAMP  NOT NULL,
    last_login  TIMESTAMP  NULL,
    is_admin boolean NOT NULL DEFAULT false,
    is_active boolean NOT NULL DEFAULT false,
    token VARCHAR ( 255 )  NULL,
    roleid int,
    is_agent boolean DEFAULT false,
    CONSTRAINT users_email_key UNIQUE (email),
    CONSTRAINT users_username_key UNIQUE (username),
    CONSTRAINT roleid FOREIGN KEY (roleid)
        REFERENCES public.roles (roleid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)
#==============Orders=============
CREATE TABLE Orders (
	orderId serial PRIMARY KEY,
	orderNumber VARCHAR ( 50 ) NOT NULL,
	orderTime TIMESTAMP  NOT NULL,
	customerId int NOT NULL ,
	orderAmount DOUBLE PRECISION  NOT NULL,
	orderLocation VARCHAR ( 255 ) NOT NULL,
	deliveryTime TIMESTAMP NULL,
	orderDetails VARCHAR ( 255 )  NULL,
	orderStatus VARCHAR ( 50 ) NOT NULL,
	deliveryAgent VARCHAR ( 50 ) NOT NULL
);

#============RegisteredCars===========
CREATE TABLE public.registeredvehicles
(
    carid serial PRIMARY KEY,
    carname  VARCHAR ( 50 ) NOT NULL,
    carmodel VARCHAR ( 50 ) NOT NULL,
    carcolor VARCHAR ( 50 ) NOT NULL,
    carregnumber VARCHAR ( 50 ) NOT NULL,
    registeredon TIMESTAMP NOT NULL,
    userid integer,
    CONSTRAINT userid FOREIGN KEY (userid)
        REFERENCES public.users (user_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)



#=========Deploying the App on Heroku=================
1. heroku login
2. touch Procfile
3. web: gunicorn ProjectName.wsgi --log-file -
4. runtime.txt and add your python e.g python-2.7.12
5. pip install gunicorn dj-database-url whitenoise psycopg2
6. pip freeze > requirements.txt
7. ROJECT_ROOT   =   os.path.join(os.path.abspath(__file__))
STATIC_ROOT  =   os.path.join(BASEDIR, 'staticfiles')
STATIC_URL = '/static/'

# Extra lookup directories for collectstatic to find static files
STATICFILES_DIRS = (
    os.path.join(BASEDIR, 'static'),
)

#  Add configuration for static files storage using whitenoise
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

