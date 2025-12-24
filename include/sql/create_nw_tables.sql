create schema if not exists nw;

CREATE TABLE if not exists nw.customers  (
	customer_id bpchar NOT NULL,
	company_name varchar(40) NOT NULL,
	contact_name varchar(30) NULL,
	contact_title varchar(30) NULL,
	address varchar(60) NULL,
	city varchar(15) NULL,
	region varchar(15) NULL,
	postal_code varchar(10) NULL,
	country varchar(15) NULL,
	phone varchar(24) NULL,
	fax varchar(24) NULL,
	CONSTRAINT pk_customers PRIMARY KEY (customer_id)
);

CREATE TABLE if not exists nw.orders (
	order_id int2 NOT NULL,
	customer_id bpchar NULL,
	employee_id int2 NULL,
	order_date date NULL,
	required_date date NULL,
	shipped_date date NULL,
	ship_via int2 NULL,
	freight float4 NULL,
	ship_name varchar(40) NULL,
	ship_address varchar(60) NULL,
	ship_city varchar(15) NULL,
	ship_region varchar(15) NULL,
	ship_postal_code varchar(10) NULL,
	ship_country varchar(15) NULL,
	CONSTRAINT pk_orders PRIMARY KEY (order_id)
);

CREATE TABLE if not exists nw.products (
	product_id int2 NOT NULL,
	product_name varchar(40) NOT NULL,
	supplier_id int2 NULL,
	category_id int2 NULL,
	quantity_per_unit varchar(20) NULL,
	unit_price float4 NULL,
	units_in_stock int2 NULL,
	units_on_order int2 NULL,
	reorder_level int2 NULL,
	discontinued int4 NOT NULL,
	CONSTRAINT pk_products PRIMARY KEY (product_id)
);

CREATE TABLE if not exists nw.order_items (
	order_id int2 NOT NULL,
	line_prod_seq int8 NULL,
	product_id int2 NOT NULL,
	amount numeric NULL,
	unit_price float4 NULL,
	quantity int2 NULL,
	discount float4 NULL,
	CONSTRAINT order_items_pk PRIMARY KEY (order_id, product_id)
);