# notes

``` python
data="s1,s2,s3,s4\n1000,1100,1300,1400\n1030,1120,1330,1440"
pd.read_csv(StringIO(data))
     s1    s2    s3    s4
0  1000  1100  1300  1400
1  1030  1120  1330  1440

data="s1,s2,s3,s4\nswindon,1000,1100,1300,1400\nkemble,1030,1120,1330,1440"
pd.read_csv(StringIO(data),index_col=0)
           s1    s2    s3    s4
swindon  1000  1100  1300  1400
kemble   1030  1120  1330  1440

df['s1']
swindon    1000
kemble     1030
Name: s1, dtype: int64

df['s2'].swindon
1100
type(df['s2'].swindon)
<class 'numpy.int64'>

for st in df['s2']:
...     print(st)
... 
1100
1120

df.index
Index(['swindon', 'kemble'], dtype='object')
for i in df.index:
...     print(i)
...     type(i)
... 
swindon
<class 'str'>
kemble
<class 'str'>
```

``` python
df.columns
Index(['s1', 's2', 's3', 's4'], dtype='object')
```