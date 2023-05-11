## Работа с классом xSV files (CSV, TSV, DSV):

a) Работа с каноническим форматом файлов CSV, TSV, DSV).

– Реализовать import/export данных из данных форматов:

a. содержит/не содержит заголовок;

b. фильтрование:

    a. по списку;
    b. по контенту (шаблон regex) в определенном поле;
    c. по контенту (шаблон regex) в нескольких полях;

c. работа с фрагментом файла:
    
    a. по строкам:
        – один диапазон;
        – несколько диапазонов * ;
    b. по столбцам;

d. данные полей:
    
    a. single string
    b. multi-string*;

e. обработка файла при нарушении канонического формата (попытаться максимально полно
получить контент) † ;

c) Реализовать пункт а)

    – by pure python string, module re (regular expression);
    – by using python module CSV.

d) Convert CSV to JSON with Python

    – by pure python module CSV and JSON;

## Results:

[csv_utility](csv_utility.py) with [CsvFileParser](CsvFileParser.py) Class

### Utility help 

![1](img/1.png)

### Support input file formats

    CSV
    TSV
    DSV (with defined delimiter)

![2](img/2.png)

![3](img/3.png)

### Support output formats to screen/file 

    CSV
    TSV
    DSV (with defined delimiter)
    JSON

![4](img/4.png)

![5](img/5.png)

### JSON without header / with header

![6](img/6.png)

![7](img/7.png)

### Columns select

```
-cols SELECTED_COLS

SELECTED_COLS:

    N         - select column N (0 - [ColCount-1])
    Start-End - select columns from Start to End
    -End      - select columns from beginning of line to End
    Start-    - select columns from Start to end of line

Examples:
    "-5,6,8-10,50-"
    "1,15,17-22,40-"
    "50-"
    "-40"
```
### Rows select

```
-rows SELECTED_ROWS

SELECTED_ROWS:

    N         - select row N (0 - [RowCount-1])
    Start-End - select rows from Start to End
    -End      - select rows from beginning of file to End
    Start-    - select rows from Start to end of file

Examples:
    "-5,6,8-10,50-"
    "1,15,17-22,40-"
    "50-"
    "-40"
```
![8](img/8.png)

### Filter on columns

```
-filter COLUMN REGEX [COLUMN REGEX ...]

Set filter REGEX on COLUMN (number or name)

Examples:

- filter 0 "\d+" Name "Oscar"
```

![f0](img/f0.png)

![f1](img/f1.png)

![f2](img/f2.png)