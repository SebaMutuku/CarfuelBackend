
 python manage.py inspectdb > models.py



-- Table: public.orders

-- DROP TABLE public.orders;

CREATE TABLE public.orders
(
    orderid integer NOT NULL DEFAULT nextval('orders_orderid_seq'::regclass),
    ordernumber character varying(50) COLLATE pg_catalog."default" NOT NULL,
    ordertime timestamp without time zone NOT NULL,
    customerid integer NOT NULL,
    orderamount double precision NOT NULL,
    orderlocation character varying(255) COLLATE pg_catalog."default" NOT NULL,
    deliverytime timestamp without time zone,
    orderdetails character varying(255) COLLATE pg_catalog."default",
    orderstatus character varying(50) COLLATE pg_catalog."default" NOT NULL,
    deliveryagent character varying(50) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT orders_pkey PRIMARY KEY (orderid),
    CONSTRAINT customerid FOREIGN KEY (customerid)
        REFERENCES public.users (user_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE public.orders
    OWNER to postgres;



-- Table: public.registeredvehicles

-- DROP TABLE public.registeredvehicles;

CREATE TABLE public.registeredvehicles
(
    carid integer NOT NULL DEFAULT nextval('registeredvehicles_carid_seq'::regclass),
    carname character varying(50) COLLATE pg_catalog."default" NOT NULL,
    carmodel character varying(50) COLLATE pg_catalog."default" NOT NULL,
    carcolor character varying(50) COLLATE pg_catalog."default" NOT NULL,
    carregnumber character varying(50) COLLATE pg_catalog."default" NOT NULL,
    registeredon timestamp without time zone NOT NULL,
    userid integer,
    CONSTRAINT registeredvehicles_pkey PRIMARY KEY (carid),
    CONSTRAINT userid FOREIGN KEY (userid)
        REFERENCES public.users (user_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE public.registeredvehicles
    OWNER to postgres;





==============-- Table: public.roles

-- DROP TABLE public.roles;

CREATE TABLE public.roles
(
    roleid integer NOT NULL DEFAULT nextval('roles_roleid_seq'::regclass),
    rolename character varying(255) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT roles_pkey PRIMARY KEY (roleid),
    CONSTRAINT roles_rolename_key UNIQUE (rolename)
)

TABLESPACE pg_default;

ALTER TABLE public.roles
    OWNER to postgres;
===================

-- Table: public.users

-- DROP TABLE public.users;

CREATE TABLE public.users
(
    user_id integer NOT NULL DEFAULT nextval('users_user_id_seq'::regclass),
    username character varying(50) COLLATE pg_catalog."default" NOT NULL,
    password character varying(50) COLLATE pg_catalog."default" NOT NULL,
    email character varying(255) COLLATE pg_catalog."default",
    created_on timestamp without time zone NOT NULL,
    last_login timestamp without time zone,
    is_admin boolean NOT NULL DEFAULT false,
    is_active boolean NOT NULL DEFAULT false,
    token character varying(255) COLLATE pg_catalog."default",
    roleid integer,
    is_agent boolean DEFAULT false,
    CONSTRAINT users_pkey PRIMARY KEY (user_id),
    CONSTRAINT users_email_key UNIQUE (email),
    CONSTRAINT users_username_key UNIQUE (username),
    CONSTRAINT roleid FOREIGN KEY (roleid)
        REFERENCES public.roles (roleid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE public.users
    OWNER to postgres;
