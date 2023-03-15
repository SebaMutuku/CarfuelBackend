# This file consists of app sql scripts
## User table sql
```sql
CREATE TABLE public.users ( user_id serial PRIMARY KEY , username VARCHAR ( 50 ) NOT NULL, password VARCHAR ( 50 ) NOT NULL, email VARCHAR ( 255 ) NULL, created_on TIMESTAMP NOT NULL, last_login TIMESTAMP NULL, is_admin boolean NOT NULL DEFAULT false, is_active boolean NOT NULL DEFAULT false, token VARCHAR ( 255 ) NULL, roleid int, is_agent boolean DEFAULT false, CONSTRAINT users_email_key UNIQUE (email), CONSTRAINT users_username_key UNIQUE (username), CONSTRAINT roleid FOREIGN KEY (roleid) REFERENCES public.roles (roleid) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION ); 
```
## Roles
```sql
CREATE TABLE Roles( roleId serial PRIMARY KEY, roleName VARCHAR (255) UNIQUE NOT NULL );
```

## Orders
```sql
CREATE TABLE Orders ( orderId serial PRIMARY KEY, orderNumber VARCHAR ( 50 ) NOT NULL, orderTime TIMESTAMP NOT NULL, customerId int NOT NULL , orderAmount DOUBLE PRECISION NOT NULL, orderLocation VARCHAR ( 255 ) NOT NULL, deliveryTime TIMESTAMP NULL, orderDetails VARCHAR ( 255 ) NULL, orderStatus VARCHAR ( 50 ) NOT NULL, deliveryAgent VARCHAR ( 50 ) NOT NULL );
```

## RegisteredCars
```sql
 CREATE TABLE public.registeredvehicles ( carid serial PRIMARY KEY, carname VARCHAR ( 50 ) NOT NULL, carmodel VARCHAR ( 50 ) NOT NULL, carcolor VARCHAR ( 50 ) NOT NULL, carregnumber VARCHAR ( 50 ) NOT NULL, registeredon TIMESTAMP NOT NULL, userid integer, CONSTRAINT userid FOREIGN KEY (userid) REFERENCES public.users (user_id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION );
```