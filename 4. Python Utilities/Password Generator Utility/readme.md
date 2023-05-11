### Write a utility for generating passwords according to a given template that supports the CLI interface and logging (-vvv – show detailed information during processing)

[Utility main code](pass.py)

[Module passwords code](passwords.py)

### Results

#### Utility run with -t TEMPLATE
![1](img/1.png)
![2](img/3.png)

#### Utility run with -t TEMPLATE with errors in template
![3](img/2.png)

#### Utility run with other errors
![4](img/11.png)

![5](img/12.png)

![6](img/13.png)


#### Utility run with -l LENGTH, with -c COUNT for -l and -t parameters
![7](img/4.png)

#### Utility run with -f FILE and -f FILE -c COUNT
![8](img/5.png)

#### Utility run with -v | -vv | -vvv

```
  -v           verbose / warning+ level
  -vv          verbose / info+ level
  -vvv         verbose / debug+ level
```
parameters

![9](img/6.png)

#### Utility run with -c COUNT without any other parameters
![10](img/9.png)


#### Utility run without parameters
![11](img/7.png)

#### Utility help 
![12](img/8.png)