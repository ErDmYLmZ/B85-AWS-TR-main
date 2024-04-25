--Table nasıl oluşturulur:
--1. Yol: Sıfırdan table oluşturma:
CREATE TABLE students
(
student_id SMALLINT,
student_name VARCHAR(50),
student_age SMALLINT,
student_dob DATE
);
--2. Yol: Başka bir table kullanarak table oluşturma:
CREATE TABLE student_name_age
AS SELECT student_name, student_age
FROM students;
SELECT * FROM student_name_age;
--Table oluştururken bazı "Constraints" atamaları yapabiliriz.
--Constraints:
--a)Unique
--b)Not Null
--c)Primary Key
--d)Foreign Key
--e)Check Constraint
--Primary Key oluşturmak için iki yol kullanabiliriz:
--1. Yol:
CREATE TABLE students
(
student_id SMALLINT PRIMARY KEY,
student_name VARCHAR(50) NOT NULL, --student_name null değer alamaz.
student_age SMALLINT,
student_dob DATE UNIQUE -->student_dob unique key ==> null değer dışındaki değerler tekrarsız olmalıdır. ÇOklu null değer atanabilir.
);
--2. Yol:
CREATE TABLE students
(
student_id SMALLINT,
student_name VARCHAR(50),
student_age SMALLINT,
student_dob DATE,
CONSTRAINT student_id_pk PRIMARY KEY(student_id)
);
--Foreign Key Constraint nasıl eklenir:
CREATE TABLE parents
(
student_id SMALLINT,
parent_name VARCHAR(50),
phone_number CHAR(11),
CONSTRAINT student_id_pk PRIMARY KEY(student_id)
);
CREATE TABLE students
(
student_id SMALLINT,
student_name VARCHAR(50),
student_age SMALLINT,
student_dob DATE,
CONSTRAINT student_id_fk FOREIGN KEY(student_id) REFERENCES parents(student_id)
);
--Check constraint nasıl eklenir:
CREATE TABLE students
(
student_id SMALLINT,
student_name VARCHAR(50),
student_age SMALLINT,
student_dob DATE,
CONSTRAINT student_age_check CHECK(student_age BETWEEN 0 AND 30),--0 ve 30 dahil
CONSTRAINT student_name_check CHECK(student_name = UPPER(student_name))
);
--Table'a veri nasıl girilir:
CREATE TABLE students
(
student_id SMALLINT PRIMARY KEY,
student_name VARCHAR(50) UNIQUE,
student_age SMALLINT NOT NULL,
student_dob DATE,
CONSTRAINT student_age_check CHECK(student_age BETWEEN 0 AND 30),
CONSTRAINT student_name_check CHECK(student_name = UPPER(student_name))
);
INSERT INTO students VALUES(101, 'ALİ CAN', 13, '10-Aug-2008' );
INSERT INTO students VALUES(102, 'VELI HAN', 14, '10-Aug-2007');
INSERT INTO students VALUES(103, 'AYSE TAN', 14, '10-Aug-2007' );
--Integer değerler single quote(tek tırnak) ile veya yalın kullanılabilir.
INSERT INTO students VALUES('104', 'KEMAL KUZU', 15, NULL );
INSERT INTO students VALUES('105', 'TOM HANKS', 15, '12-Sep-1996' );
INSERT INTO students VALUES('106', 'ANGELINA JULIE', 30, '12-Sep-1987' );
INSERT INTO students VALUES('107', 'BRAD PITT', 0, '26-Jul-2022' );
--Spesifik bir sütuna veri nasıl girilir:
INSERT INTO students(student_id, student_age) VALUES(108, 17);
INSERT INTO students(student_name, student_id, student_age) VALUES('JOHN WALKER', 109, 24);
--Varolan bir data nasıl değiştirilir:
UPDATE students
SET student_name = 'LEO OCEAN'
WHERE student_id = 108;
SELECT * FROM students;
