drop DATABASE IF exists commerce;

create DATABASE commerce;

USE commerce;

create table User(
 id INT NOT NULL AUTO_INCREMENT,
 name VARCHAR (50) NOT NULL,
 cpf CHAR(11) NOT NULL,
 PRIMARY KEY (id),
 UNIQUE (cpf)
) ENGINE = INNODB;

create table Client(
 id_user INT NOT NULL,
 surname VARCHAR (50)NOT NULL,
 status BOOLEAN NOT NULL
) ENGINE = INNODB;

create table Clerk(
 id_user INT NOT NULL,
 email VARCHAR (100) NOT NULL,
 password VARCHAR (20) NOT NULL
) ENGINE = INNODB;

create table Address(
 id INT NOT NULL AUTO_INCREMENT,
 id_client INT NOT NULL,
 public_place VARCHAR (100) NOT NULL,
 number VARCHAR (5) NOT NULL,
 zip_code CHAR(9),
 PRIMARY KEY (id),
 UNIQUE (id_client)
) ENGINE = INNODB;

create table Phone(
 id_cpf CHAR(11) NOT NULL,
 phone_number CHAR(11) NOT NULL,
 notification BOOLEAN NOT NULL
) ENGINE = INNODB;

create table Product(
 id INT NOT NULL AUTO_INCREMENT,
 title VARCHAR (20),
 name VARCHAR (10) NOT NULL,
 price DECIMAL (3,2) NOT NULL,
 code VARCHAR (10) NOT NULL,
 PRIMARY KEY (code),
 KEY (id)
) ENGINE = INNODB;

create table Demand (
  id INT NOT NULL AUTO_INCREMENT,
  date DATE NOT NULL,
  time TIME NOT NULL,
  id_client INT NOT NULL,
  id_clerk INT NOT NULL,
  PRIMARY KEY (id)
) ENGINE = INNODB;

create table Item(
 id_demand INT NOT NULL,
 id_product INT NOT NULL,
 quantity NUMERIC (10,2) NOT NULL,
 PRIMARY KEY (id_demand,id_product)
) ENGINE = INNODB;


ALTER TABLE Address ADD CONSTRAINT FK_Address_User
 FOREIGN KEY (id_client) REFERENCES User(id)
  ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE Phone ADD CONSTRAINT FK_Phone_User
 FOREIGN KEY (id_cpf) REFERENCES User(cpf)
  ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE Demand ADD CONSTRAINT FK_Demand_User
 FOREIGN KEY (id_client) REFERENCES User(id)
  ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE Item ADD CONSTRAINT FK_Item_Demand
 FOREIGN KEY (id_demand) REFERENCES Demand(id)
  ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE Item ADD CONSTRAINT FK_Item_Product
 FOREIGN KEY (id_product) REFERENCES Product(id)
  ON DELETE RESTRICT ON UPDATE RESTRICT;


INSERT INTO User (name, cpf) VALUES("Dorothy","72259372007");
INSERT INTO Client (id,surname, status) VALUES(1,"King",TRUE);

INSERT INTO User (name, cpf) VALUES("Jon","68709620060");
INSERT INTO Client (id,surname, status) VALUES(2,"Nkoma",TRUE);

INSERT INTO User (name, cpf) VALUES("Won","87283561013");
INSERT INTO Client (id,surname, status) VALUES(3,"Lau",TRUE);

INSERT INTO User (name, cpf) VALUES("Bert","56603582090");
INSERT INTO Client (id,surname, status) VALUES(4,"Kovalsco",TRUE);

INSERT INTO User (name, cpf) VALUES("Tom","56309984047");
INSERT INTO Client (id,surname, status) VALUES(5,"Quercos",TRUE);

INSERT INTO User (name, cpf) VALUES("Jimmy","27605414013");
INSERT INTO Client (id,surname, status) VALUES(6,"Chan",TRUE);

INSERT INTO User (name, cpf) VALUES("Jane","89576228026");
INSERT INTO Client (id,surname, status) VALUES(7,"East",TRUE);

INSERT INTO User (name, cpf) VALUES("Caelan","63755750449");
INSERT INTO Client (id,surname, status) VALUES(8,"Corrigan",TRUE);


INSERT INTO User (name, cpf) VALUES("Renan","78234924400");
INSERT INTO Clerk(id,email, password) VALUES(9,"renan@vendinha.com","passwd123");

INSERT INTO User (name, cpf) VALUES("Ruan","43367999466");
INSERT INTO Clerk(id, email, password) VALUES(10,"ruan@vendinha.com","passwd456");

INSERT INTO User (name, cpf) VALUES("Nonato","31710548410");
INSERT INTO Clerk(id, email, password) VALUES(11, "nonato@vendinha.com","passwd789");



INSERT INTO Address (id_client,public_place,number,zip_code) VALUES(1,"Passagem Gama Malcher","482","66085390");
INSERT INTO Address (id_client,public_place,number,zip_code) VALUES(2,"Passagem Nossa Senhora de Fátima","964","66842130");
INSERT INTO Address (id_client,public_place,number,zip_code) VALUES(3,"Vila Carlos","562","66645565");
INSERT INTO Address (id_client,public_place,number,zip_code) VALUES(4,"Vila Isaías da Paz","789","66015150");
INSERT INTO Address (id_client,public_place,number,zip_code) VALUES(5,"Passagem Maria da Glória","650","66840230");
INSERT INTO Address (id_client,public_place,number,zip_code) VALUES(6,"Quadra WR-18","218","66630287");
INSERT INTO Address (id_client,public_place,number,zip_code) VALUES(7,"Passagem de Santa Rita Cassia","896","66810085");
INSERT INTO Address (id_client,public_place,number,zip_code) VALUES(8,"Ladeira do Castelo","124","66020170");

INSERT INTO Phone (id_cpf, phone_number, notification) VALUES("72259372007","91984292065",TRUE);
INSERT INTO Phone (id_cpf, phone_number, notification) VALUES("68709620060","91996288947",TRUE);
INSERT INTO Phone (id_cpf, phone_number, notification) VALUES("87283561013","91996937507",TRUE);
INSERT INTO Phone (id_cpf, phone_number, notification) VALUES("56603582090","91999461580",TRUE);
INSERT INTO Phone (id_cpf, phone_number, notification) VALUES("56309984047","91992099760",TRUE);
INSERT INTO Phone (id_cpf, phone_number, notification) VALUES("27605414013","91985174469",TRUE);
INSERT INTO Phone (id_cpf, phone_number, notification) VALUES("89576228026","91995788281",TRUE);
INSERT INTO Phone (id_cpf, phone_number, notification) VALUES("63755750449","91994948439",TRUE);
INSERT INTO Phone (id_cpf, phone_number, notification) VALUES("31710548410","91983087414",TRUE);


INSERT INTO Product (title, name, price, code) VALUES("Arroz","Fazanda",3.50,'1');
INSERT INTO Product (title, name, price, code) VALUES("Arroz","Tio João",3.00,'2');
INSERT INTO Product (title, name, price, code) VALUES("Feijão carioca","Tio pedro",5.50,'3');
INSERT INTO Product (title, name, price, code) VALUES("Feijão cavalo","São pedro",6.50,'4');
INSERT INTO Product (title, name, price, code) VALUES("Macarão","Hiléia",3.50,'5');
INSERT INTO Product (title, name, price, code) VALUES("Óleo","Primor",4.00,'6');
INSERT INTO Product (title, name, price, code) VALUES("Açúcar","Pricesa",3.20,'7');
INSERT INTO Product (title, name, price, code) VALUES("Leite","Dubom",3.50,'8');


INSERT INTO Demand (date, time, id_client, id_clerk) VALUES((SELECT CURRENT_DATE()), (SELECT CURRENT_TIME()),1,1);
INSERT INTO Item (id_demand,id_product,quantity) VALUES(1,2,2);
INSERT INTO Item (id_demand,id_product,quantity) VALUES(1,3,1);
INSERT INTO Item (id_demand,id_product,quantity) VALUES(1,6,1);
INSERT INTO Item (id_demand,id_product,quantity) VALUES(1,7,1.5);
INSERT INTO Item (id_demand,id_product,quantity) VALUES(1,5,0.5);
INSERT INTO Item (id_demand,id_product,quantity) VALUES(1,8,1);


INSERT INTO Demand (date, time, id_client, id_clerk) VALUES((SELECT CURRENT_DATE()), (SELECT CURRENT_TIME()),2,1);
INSERT INTO Item (id_demand,id_product,quantity) VALUES(2,2,2);
INSERT INTO Item (id_demand,id_product,quantity) VALUES(2,5,1);
INSERT INTO Item (id_demand,id_product,quantity) VALUES(2,7,1.5);
INSERT INTO Item (id_demand,id_product,quantity) VALUES(2,8,1);

INSERT INTO Demand (date, time, id_client, id_clerk) VALUES((SELECT CURRENT_DATE()), (SELECT CURRENT_TIME()),3,1);
INSERT INTO Item (id_demand,id_product,quantity) VALUES(3,7,1.5);
INSERT INTO Item (id_demand,id_product,quantity) VALUES(3,5,0.5);
INSERT INTO Item (id_demand,id_product,quantity) VALUES(3,8,1);

INSERT INTO Demand (date, time, id_client, id_clerk) VALUES((SELECT CURRENT_DATE()), (SELECT CURRENT_TIME()),7,2);
INSERT INTO Item (id_demand,id_product,quantity) VALUES(4,2,2);
INSERT INTO Item (id_demand,id_product,quantity) VALUES(4,5,1);
INSERT INTO Item (id_demand,id_product,quantity) VALUES(4,7,1.5);
INSERT INTO Item (id_demand,id_product,quantity) VALUES(4,8,1);




