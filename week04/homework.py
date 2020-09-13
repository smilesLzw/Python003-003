"""
参考同学，能理解，等熟悉 sql 再进行修改
"""

import pandas as pd

# 1. SELECT * FROM data;                                                    
df = pd.read_csv(data)
 
# 2. SELECT * FROM data LIMIT 10;
data[:10]
 
# 3. SELECT id FROM data;  //id 是 data 表的特定一列
data.iloc[:,['id']]
 
# 4. SELECT COUNT(id) FROM data;
data.count('id')
 
# 5. SELECT * FROM data WHERE id<1000 AND age>30;
data[data['id'] < 1000 and data['age'] > 30 ]
 
# 6. SELECT id,COUNT(DISTINCT order_id) FROM table1 GROUP BY id;
table1.groupby('id').['order_id'].nunique()
 
# 7. SELECT * FROM table1 t1 INNER JOIN table2 t2 ON t1.id = t2.id;
pd.merge(t1, t2, left_on='id',right_on='id',how='inner')
 
# 8. SELECT * FROM table1 UNION SELECT * FROM table2;
pd.concat([table1 ,table2])
 
# 9. DELETE FROM table1 WHERE id=10;
table1.drop(table1[table1['id'] = 10].index)
 
# 10. ALTER TABLE table1 DROP COLUMN column_name;
table1.drop(['column_name'])