# notes

``` python
import pandas as pd
import numpy as np
from io import StringIO

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
df.index
df.index[1]
len(df.index)

```

``` python
import matplotlib.pyplot as plt

df = pd.DataFrame({'period': [1, 2, 3, 4, 5, 6, 7, 8],
                   'A': [9, 12, 15, 14, 19, 23, 25, 29],
                   'B': [5, 7, 7, 9, 12, 9, 9, 14],
                   'C': [5, 4, 7, 13, 15, 15, 18, 31]})
df[['period', 'A']].plot(x='A', y='period', kind='scatter')
plt.show()

plt.scatter(df['A'],df['period'])
plt.plot(df['A'],df['period'])
plt.show()
```

``` python working example
>>> data="dist,s1,s2,s3,s4\nswindon,75.2,1000,1100,1300,1400\nkemble,80.0,1030,1120,1330,1440"
>>> pd.read_csv(StringIO(data),index_col=0)
         dist    s1    s2    s3    s4
swindon  75.2  1000  1100  1300  1400
kemble   80.0  1030  1120  1330  1440
>>> timetable = pd.read_csv(StringIO(data),index_col=0)
>>> t = pd.read_csv(StringIO(data),index_col=0)
>>> plt.plot(t['s1'],t['dist'])
[<matplotlib.lines.Line2D object at 0x7fefa17ccd30>]
>>> plt.show()
>>> plt.plot(t['s1'],t['dist'])
[<matplotlib.lines.Line2D object at 0x7fefa174be20>]
>>> plt.plot(t['s2'],t['dist'])
[<matplotlib.lines.Line2D object at 0x7fefa175c2e0>]
>>> plt.plot(t['s3'],t['dist'])
[<matplotlib.lines.Line2D object at 0x7fefa175c790>]
>>> plt.show()
```

