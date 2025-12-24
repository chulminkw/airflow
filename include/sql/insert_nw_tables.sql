INSERT INTO nw.customers (customer_id,company_name,contact_name,contact_title,address,city,region,postal_code,country,phone,fax) VALUES
	 ('BSBEV','B''s Beverages','Victoria Ashworth','Sales Representative','Fauntleroy Circus','London',NULL,'EC2 5NT','UK','(171) 555-1212',NULL),
	 ('CACTU','Cactus Comidas para llevar','Patricio Simpson','Sales Agent','Cerrito 333','Buenos Aires',NULL,'1010','Argentina','(1) 135-5555','(1) 135-4892'),
	 ('CENTC','Centro comercial Moctezuma','Francisco Chang','Marketing Manager','Sierras de Granada 9993','M?xico D.F.',NULL,'05022','Mexico','(5) 555-3392','(5) 555-7293'),
	 ('CHOPS','Chop-suey Chinese','Yang Wang','Owner','Hauptstr. 29','Bern',NULL,'3012','Switzerland','0452-076545',NULL),
	 ('COMMI','Com?rcio Mineiro','Pedro Afonso','Sales Associate','Av. dos Lus?adas, 23','Sao Paulo','SP','05432-043','Brazil','(11) 555-7647',NULL),
	 ('CONSH','Consolidated Holdings','Elizabeth Brown','Sales Representative','Berkeley Gardens 12  Brewery','London',NULL,'WX1 6LT','UK','(171) 555-2282','(171) 555-9199'),
	 ('DRACD','Drachenblut Delikatessen','Sven Ottlieb','Order Administrator','Walserweg 21','Aachen',NULL,'52066','Germany','0241-039123','0241-059428'),
	 ('DUMON','Du monde entier','Janine Labrune','Owner','67, rue des Cinquante Otages','Nantes',NULL,'44000','France','40.67.88.88','40.67.89.89'),
	 ('EASTC','Eastern Connection','Ann Devon','Sales Agent','35 King George','London',NULL,'WX3 6FW','UK','(171) 555-0297','(171) 555-3373'),
	 ('ERNSH','Ernst Handel','Roland Mendel','Sales Manager','Kirchgasse 6','Graz',NULL,'8010','Austria','7675-3425','7675-3426');

INSERT INTO nw.products (product_id,product_name,supplier_id,category_id,quantity_per_unit,unit_price,units_in_stock,units_on_order,reorder_level,discontinued) VALUES
	 (1,'Chai',8,1,'10 boxes x 30 bags',18.0,39,0,10,1),
	 (2,'Chang',1,1,'24 - 12 oz bottles',19.0,17,40,25,1),
	 (3,'Aniseed Syrup',1,2,'12 - 550 ml bottles',10.0,13,70,25,0),
	 (4,'Chef Anton''s Cajun Seasoning',2,2,'48 - 6 oz jars',22.0,53,0,0,0),
	 (5,'Chef Anton''s Gumbo Mix',2,2,'36 boxes',21.35,0,0,0,1),
	 (6,'Grandma''s Boysenberry Spread',3,2,'12 - 8 oz jars',25.0,120,0,25,0),
	 (7,'Uncle Bob''s Organic Dried Pears',3,7,'12 - 1 lb pkgs.',30.0,15,0,10,0),
	 (8,'Northwoods Cranberry Sauce',3,2,'12 - 12 oz jars',40.0,6,0,0,0),
	 (9,'Mishi Kobe Niku',4,6,'18 - 500 g pkgs.',97.0,29,0,0,1),
	 (10,'Ikura',4,8,'12 - 200 ml jars',31.0,31,0,0,0);
	
INSERT INTO nw.orders (order_id,customer_id,employee_id,order_date,required_date,shipped_date,ship_via,freight,ship_name,ship_address,ship_city,ship_region,ship_postal_code,ship_country) VALUES
	 (10248,'VINET',5,'1996-07-04','1996-08-01','1996-07-16',3,32.38,'Vins et alcools Chevalier','59 rue de l''Abbaye','Reims',NULL,'51100','France'),
	 (10249,'TOMSP',6,'1996-07-05','1996-08-16','1996-07-10',1,11.61,'Toms Spezialit?ten','Luisenstr. 48','M?nster',NULL,'44087','Germany'),
	 (10250,'HANAR',4,'1996-07-08','1996-08-05','1996-07-12',2,65.83,'Hanari Carnes','Rua do Pa?o, 67','Rio de Janeiro','RJ','05454-876','Brazil'),
	 (10251,'VICTE',3,'1996-07-08','1996-08-05','1996-07-15',1,41.34,'Victuailles en stock','2, rue du Commerce','Lyon',NULL,'69004','France'),
	 (10252,'SUPRD',4,'1996-07-09','1996-08-06','1996-07-11',2,51.3,'Supr?mes d?lices','Boulevard Tirou, 255','Charleroi',NULL,'B-6000','Belgium'),
	 (10253,'HANAR',3,'1996-07-10','1996-07-24','1996-07-16',2,58.17,'Hanari Carnes','Rua do Pa?o, 67','Rio de Janeiro','RJ','05454-876','Brazil'),
	 (10254,'CHOPS',5,'1996-07-11','1996-08-08','1996-07-23',2,22.98,'Chop-suey Chinese','Hauptstr. 31','Bern',NULL,'3012','Switzerland'),
	 (10255,'RICSU',9,'1996-07-12','1996-08-09','1996-07-15',3,148.33,'Richter Supermarkt','Starenweg 5','Gen?ve',NULL,'1204','Switzerland'),
	 (10256,'WELLI',3,'1996-07-15','1996-08-12','1996-07-17',2,13.97,'Wellington Importadora','Rua do Mercado, 12','Resende','SP','08737-363','Brazil'),
	 (10257,'HILAA',4,'1996-07-16','1996-08-13','1996-07-22',3,81.91,'HILARION-Abastos','Carrera 22 con Ave. Carlos Soublette #8-35','San Crist?bal','T?chira','5022','Venezuela');
	
INSERT INTO nw.order_items (order_id,line_prod_seq,product_id,amount,unit_price,quantity,discount) VALUES
	 (10248,1,11,168.00,14.0,12,0.0),
	 (10248,2,42,98.00,9.8,10,0.0),
	 (10248,3,72,174.00,34.8,5,0.0),
	 (10249,1,14,167.40,18.6,9,0.0),
	 (10249,2,51,1696.00,42.4,40,0.0),
	 (10250,1,41,77.00,7.7,10,0.0),
	 (10250,2,51,1261.40,42.4,35,0.15),
	 (10250,3,65,214.20,16.8,15,0.15),
	 (10251,1,22,95.76,16.8,6,0.05),
	 (10251,2,57,222.30,15.6,15,0.05);	
	
INSERT INTO nw.orders (order_id,customer_id,employee_id,order_date,required_date,shipped_date,ship_via,freight,ship_name,ship_address,ship_city,ship_region,ship_postal_code,ship_country) VALUES
	 (10258,'ERNSH',1,'1996-07-17','1996-08-14','1996-07-23',1,140.51,'Ernst Handel','Kirchgasse 6','Graz',NULL,'8010','Austria'),
	 (10259,'CENTC',4,'1996-07-18','1996-08-15','1996-07-25',3,3.25,'Centro comercial Moctezuma','Sierras de Granada 9993','M?xico D.F.',NULL,'05022','Mexico'),
	 (10260,'OTTIK',4,'1996-07-19','1996-08-16','1996-07-29',1,55.09,'Ottilies K?seladen','Mehrheimerstr. 369','K?ln',NULL,'50739','Germany'),
	 (10261,'QUEDE',4,'1996-07-19','1996-08-16','1996-07-30',2,3.05,'Que Del?cia','Rua da Panificadora, 12','Rio de Janeiro','RJ','02389-673','Brazil'),
	 (10262,'RATTC',8,'1996-07-22','1996-08-19','1996-07-25',3,48.29,'Rattlesnake Canyon Grocery','2817 Milton Dr.','Albuquerque','NM','87110','USA'),
	 (10263,'ERNSH',9,'1996-07-23','1996-08-20','1996-07-31',3,146.06,'Ernst Handel','Kirchgasse 6','Graz',NULL,'8010','Austria'),
	 (10264,'FOLKO',6,'1996-07-24','1996-08-21','1996-08-23',3,3.67,'Folk och f? HB','?kergatan 24','Br?cke',NULL,'S-844 67','Sweden'),
	 (10265,'BLONP',2,'1996-07-25','1996-08-22','1996-08-12',1,55.28,'Blondel p?re et fils','24, place Kl?ber','Strasbourg',NULL,'67000','France'),
	 (10266,'WARTH',3,'1996-07-26','1996-09-06','1996-07-31',3,25.73,'Wartian Herkku','Torikatu 38','Oulu',NULL,'90110','Finland'),
	 (10267,'FRANK',4,'1996-07-29','1996-08-26','1996-08-06',1,208.58,'Frankenversand','Berliner Platz 43','M?nchen',NULL,'80805','Germany');