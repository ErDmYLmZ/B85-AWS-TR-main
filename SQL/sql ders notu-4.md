CREATE TABLE employees
(
  id CHAR(9),
  name VARCHAR(50),
  state VARCHAR(50),
  salary SMALLINT,
  company VARCHAR(20)
);
​
INSERT INTO employees VALUES(123456789, 'John Walker', 'Florida', 2500, 'IBM');
INSERT INTO employees VALUES(234567890, 'Brad Pitt', 'Florida', 1500, 'APPLE');
INSERT INTO employees VALUES(345678901, 'Eddie Murphy', 'Texas', 3000, 'IBM');
INSERT INTO employees VALUES(456789012, 'Eddie Murphy', 'Virginia', 1000, 'GOOGLE');
INSERT INTO employees VALUES(567890123, 'Eddie Murphy', 'Texas', 7000, 'MICROSOFT');
INSERT INTO employees VALUES(456789012, 'Brad Pitt', 'Texas', 1500, 'GOOGLE');
INSERT INTO employees VALUES(123456710, 'Mark Stone', 'Pennsylvania', 2500, 'IBM');
​
SELECT * FROM employees;
​
CREATE TABLE companies
(
  company_id CHAR(9),
  company VARCHAR(20),
  number_of_employees SMALLINT
);
​
INSERT INTO companies VALUES(100, 'IBM', 12000);
INSERT INTO companies VALUES(101, 'GOOGLE', 18000);
INSERT INTO companies VALUES(102, 'MICROSOFT', 10000);
INSERT INTO companies VALUES(103, 'APPLE', 21000);
​
SELECT * FROM companies;
​
--Herbir company için company, number_of_employees ve ortalama salary değerlerini bulun.
​
SELECT company, number_of_employees, (SELECT AVG(salary) FROM employees
                                     WHERE companies.company = employees.company) AS avg_salary_per_company
​
FROM companies;
​
--Herbir company için company_id, company,  en yüksek ve en düşük salary değerlerini bulun.
​
SELECT company_id, company, (SELECT MAX(salary) FROM employees  WHERE companies.company = employees.company),
                            (SELECT MIN(salary) FROM employees  WHERE companies.company = employees.company)
​
FROM companies;
​
​
--LIKE Condition: Wildcard ile kullanılır.
​
--1) % Wildcard: Sıfır yada daha fazla karakteri temsil eder.
​
-- 'E' ile başlayan employee 'name' değerlerini çağırın.
​
SELECT name
FROM employees
WHERE name LIKE 'E%';
​
​
--'e' ile biten employee 'name' değerlerini çağırın.
​
SELECT name
FROM employees
WHERE name LIKE '%e';
​
--'B' ile başlayıp 't' ile biten employee 'name' değerlerini çağırın.
SELECT name
FROM employees
WHERE name LIKE 'B%t';
​
-- Herhangi bir yerinde 'a' bulunan employee 'name' değerlerini çağırın.
SELECT name
FROM employees
WHERE name LIKE '%a%';
​
--Herhangi bir yerinde 'e' veya 'r' bulunan employee 'name' değerlerini çağırın.
SELECT name
FROM employees
WHERE name LIKE '%r%e%' OR name LIKE '%e%r%';
​
--2) _ Wildcard: Tek karakteri temsil eder.
​
--İkinci karakteri 'e' ve dördüncü karakteri 'n' olan "state" değerlerini çağırın.
SELECT state
FROM employees
WHERE state LIKE '_e_n%';
​
--Sondan ikinci karakteri 'i' olan "state" değerlerini çağırın.
SELECT state
FROM employees
WHERE state LIKE '%i_';
​
--İkinci karakteri 'e' olan ve en az 6 karakteri bulunan "state" değerlerini çağırın.
SELECT state
FROM employees
WHERE state LIKE '_e____%';
​
--İkinci karakterinden sonra herhangi bir yerinde 'i' bulunan "state" değerlerini çağırın.
SELECT state
FROM employees
WHERE state LIKE '__%i%';
​
​
CREATE TABLE words
(
  word_id CHAR(10) UNIQUE,
  word VARCHAR(50) NOT NULL,
  number_of_letters SMALLINT
);
​
INSERT INTO words VALUES (1001, 'hot', 3);
INSERT INTO words VALUES (1002, 'hat', 3);
INSERT INTO words VALUES (1003, 'hit', 3);
INSERT INTO words VALUES (1004, 'hbt', 3);
INSERT INTO words VALUES (1008, 'hct', 3);
INSERT INTO words VALUES (1005, 'adem', 4);
INSERT INTO words VALUES (1006, 'selena', 6);
INSERT INTO words VALUES (1007, 'yusuf', 5);
​
​
--NOT LIKE Condition
​
--Herhangi bir yerinde 'h' bulunmayan "word" değerlerini çağırın.
​
SELECT word
FROM words
WHERE word NOT LIKE '%h%';
​
--'t' veya 'f' ile bitmeyen "word" değerlerini çağırın.
SELECT word
FROM words
WHERE word NOT LIKE '%t' AND  word NOT LIKE '%f';
​
--Hergangi bir karakterle başlayıp 'a' veya 'e' ile devam etmeyen "word" değerlerini çağırın.
SELECT word
FROM words
WHERE word NOT LIKE '_a%' AND word NOT LIKE '_e%';
​
​
--Regular Expression Condition:
--İlk karakteri 'h', ikinci karakteri 'o', 'a' veya 'i', son karakteri 't' ve  olan "word" değerlerini çağırın.
--1. Yol: LIKE Kullanarak ==> Tekrar sebebi ile tavsiye edilmez.
SELECT word
FROM words
WHERE word LIKE 'ho%t' OR word LIKE 'ha%t' OR word LIKE 'hi%t';
​
--2. Yol: Regex kullanarak
SELECT word
FROM words
WHERE word ~ 'h[oai](.*)t';
​
--İlk karakteri 'h', son karakteri 't' ve ikinci karakteri 'a'dan 'e'ye herhangi bir karakter olan "word" değerlerini çağırın.
SELECT word
FROM words
WHERE word ~ 'h[a-e](.*)t';--[a-e]==> a, b, c, d, e
​
--İlk karakteri 's', 'a' veya 'y' olan "word" değerlerini çağırın.
SELECT word
FROM words
WHERE word ~ '^[say](.*)';
​
--Son karakteri 'm', 'a' veya 'f' olan "word" değerlerini çağırın.
SELECT word
FROM words
WHERE word ~ '(.*)[maf]$';-->(.*) isteğe bağlı
​
--İlk karakteri 's' ve son karakteri 'a' olan "word" değerlerini çağırın.
SELECT word
FROM words
WHERE word ~ 's(.*)a';--(.*) ==> ifadesi sıfır yada çoklu karakterler için kullanılır.
​
--Herhangi bir yerinde 'a' olan "word" değerlerini çağırın.
SELECT word
FROM words
WHERE word ~ 'a'; --> 'a' ==> %a%
​
--İlk karakteri 'd' den 't' ye olan, herhangi bir karakter ile devam edip üçüncü karakteri 'l' olan "word" değerlerini çağırın.
SELECT word
FROM words
WHERE word ~ '^[d-t].l';
​
--İlk karakteri 'd' den 't' ye olan,  herhangi iki karakter ile devam edip dördüncü karakteri 'e' olan "word" değerlerini çağırın.
SELECT word
FROM words
WHERE word ~ '^[d-t]..e(.*)';
​
​
CREATE TABLE workers
(
  id CHAR(9),
  name VARCHAR(50),
  state VARCHAR(50),
  salary SMALLINT,
  company VARCHAR(20)
);
​
INSERT INTO workers VALUES(123456789, 'John Walker', 'Florida', 2500, 'IBM');
INSERT INTO workers VALUES(234567890, 'Brad Pitt', 'Florida', 1500, 'APPLE');
INSERT INTO workers VALUES(345678901, 'Eddie Murphy', 'Texas', 3000, 'IBM');
INSERT INTO workers VALUES(456789012, 'Eddie Murphy', 'Virginia', 1000, 'GOOGLE');
INSERT INTO workers VALUES(567890123, 'Eddie Murphy', 'Texas', 7000, 'MICROSOFT');
INSERT INTO workers VALUES(456789012, 'Brad Pitt', 'Texas', 1500, 'GOOGLE');
INSERT INTO workers VALUES(123456710, 'Mark Stone', 'Pennsylvania', 2500, 'IBM');
​
​
--'E' başlayıp ve 'y' biten "name" değerleri dışındaki "name" değerlerini çağırın.
--1. Yol: NOT LIKE kullanarak (Ödev)
​
​
--2. Yol:
SELECT name
FROM workers
WHERE name ~ '^[^E](.*)[^y]$';--> Köşeli parantez içinde ^ kullanırsanız " 'den farklı " anlamına gelir.
​
--'E' ile başlayıp 'y' ile ile biten "name" değerlerini çağırın.(Ödev)
​
--'J', 'B' yada 'E' ile başlayan VE 'r' yada 't' ile biten "name" değerlerini çağırın.
SELECT name
FROM workers
WHERE name ~ '^[JBE](.*)[rt]$';
​
​
-- Son karakteri 'r' yada 't' olan VEYA ilk karakteri 'J','B', yada 'E' olan "name" değerlerini çağırın.
SELECT name
FROM workers
WHERE name ~ '^[JBE]' OR name ~ '[rt]$';
​
​
--Son karakteri 'r' yada 't' olmayan VE ilk karakteri 'J','B', yada 'E' olmayan "name" değerlerini çağırın.
SELECT name
FROM workers
WHERE name ~ '^[^JBE](.*)[^rt]$';
​
--Son karakteri 'r' yada 't' olmayan VEYA ilk karakteri 'J','B', yada 'E' olmayan "name" değerlerini çağırın.
SELECT name
FROM workers
WHERE name ~ '^[^JBE]' OR name ~ '[^rt]$';
​
--Herhangi bir yerinde 'a' bulunan "name" değerlerini çağırın.(Ödev)
​
​
--Herhangi bir yerinde 'a' yada 'k' bulunan "name" değerlerini çağırın.
SELECT name
FROM workers
WHERE name ~ '[ak]';
​
--İlk harfi 'A' dan 'F' ye bir karakter olan ve ikinci harfi herhangi bir karakter olup üçüncü harfi 'a' olan "name" değerlerini çağırın.
​
SELECT name
FROM workers
WHERE name ~ '^[A-F].a(.*)';
​
--İlk harfi 'A' dan 'F' ye bir karakter olan ve ikinci ve üçüncü harfi herhangi bir karakter olup dördüncü harfi 'i' olan "name" değerlerini çağırın.(Ödev)
​
--Üçüncü karakteri 'o' yada 'x' olan "state" değerlerini çağırın.
SELECT state
FROM workers
WHERE state ~ '..[ox]';
​
-- Üçüncü karakteri 'o' yada 'x' olmayan "state" değerlerini çağırın.
SELECT state
FROM workers
WHERE state ~ '^..[^ox]';
​
--Sondan üçüncü karakteri 'n' yada 'x' olan  "state" değerlerini çağırın.(Ödev)
​
--Sondan üçüncü karakteri 'n' yada 'x' olmayan  "state" değerlerini çağırın.(Ödev)
​
​
--ORDER BY: Recordları artan yada azalan düzende sıralamak için kullanılır.
--          ORDER BY sadece SELECT Statement ile kullanılır.
​
--Recordları artan düzende number_of_letters değerine göre sıralayın.
SELECT *
FROM words
ORDER BY number_of_letters;--ASC keyword'u zorunlu değildir. Çünkü artan sıralama varsayılan sıralama tipidir.
​
--Recordları azalan düzende "word" sürununa göre sıralayın.
SELECT *
FROM words
ORDER BY word DESC;--Azalan sıralamalarda DESC keywordunu yazmak zorunludur.
​
--Not: Sütun adı yerine sütun numarası ile de sıralama yapabiliriz.
SELECT *
FROM words
ORDER BY 3 DESC;-->3, number_of_letters yerine geçer.
​
​
​
SELECT * FROM words;
