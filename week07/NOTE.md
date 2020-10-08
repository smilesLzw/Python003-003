# 学习笔记

## 类属性和对象属性

类的两大成员：属性和方法

### 属性

- 类属性和对象属性
- 类属性字段在内存中只保存一份
- 对象属性在每个对象中都保存一份

```python
class Human():
    # 人为约定不可修改
    _age = 0
    
    # 私有属性
    __fly = True
    
    # 魔术方法，不会自动改名
    # 如 __init__
```

### 类的属性作用域

#### 作用域

- _name 认为约定不可修改
- __name  私有属性
- __name__ 魔术方法

#### 魔术方法：

- 双下划线开头和结尾的方法，实现了类的特殊成员，这类称作魔术方法
- 不是所有的双下划线开头和结尾的方法都是魔术方法
- 魔术方法类似其他语言的接口

私有属性是可以访问到的，Python 通过改名机制隐藏了变量名称

- class.__dict__

为类添加静态字段

```python
class Human():
    pass
    
Huanm.newattr = 1
dir(Human)
Human.__dict__
```

**注意**

内置类型不能增加属性和方法


---


三种方法

- 普通方法：至少一个 self 参数，表示该方法的对象
- 类方法：至少一个 cls 参数，表示该方法的类
- 静态方法：由类调用，无参数

三种方法在内存中都归属于类

### 类方法描述器

#### classmethod

classmethod 是一个构造函数，因为 `class` 里面默认只有一个 `__new__` 构造函数，很多时候不够用，我们就会根据需求来进行增加

##### classmethod 的两大应用场景

- 定义到父类之中，当你使用子类的时候，子类如果需要去根据自己的变量名称发生变化的时候，子类就可以引用到父类的 classmethod
- 当你的函数需要去调用类，并且返回类的时候

##### @classmethon 示例

```
# 传统写法
class Ks2(object):
    def __init__(self, fname, lname):
        self.fname = fname
        self.lname = lname
        
    def print_name(self):
        print(f'first name is {self.fname}')
        print(f'last name is {self.lname}')
        
def pre_name(obj, name):
    fname, lname = name.split('-')
    return obj(fname, lname)

m2 = pre_name(Ks2, 'wilson-yin')
m2.print_name()
```

使用类方法

```
# 改进
class Ks3(object):
    def __init__(self, fname, lname):
        self.fname = fname
        self.lname = lname
        
    @classmethod
    def pre_name(cls, name):
        fname, lname = name.split('-')
        return cls(fname, lname)
    
    def print_name(self):
        print(f'first name is {self.fname}')
        print(f'last name is {self.lname}')
        
        
m3 = Ks3.pre_name('wilson-yin')
m3.print_name()
```

### 静态方法描述器

让我们定义好的函数和我们的类产生一定的关系,
因为 staticmethod 修饰的函数不带任何参数，既不带 `self`，又不带 `cls(class)`，因此我们在实例和使用类的时候，staticmethod 修饰的方法不能用到类和实例的属性

#### 作用

- 用 staticmethod 修饰的函数做一些功能的转换


### 特殊属性和方法

#### `__init__()`
- `__init__()` 方法所做的工作是在类的对象创建好之后进行变量的初始化。 
- `__init__()` 方法不需要显式返回，默认为 None，否则会在运行时抛出 TypeError。

#### self()

- self 表示实例对象本身
- self 不是 Python 的关键字（cls也不是），可以将 self 替换成任何你喜欢的名称，
如 this、obj 等，实际效果和 self 是一样的（不推荐）。 
- 在方法声明时，需要定义 self 作为第一个参数，调用方法的时候不用传入 self。

### 属性的处理

在类中，需要对实例获取属性这一行为进行操作，可以使用：

- `__getattribute__()` 
- `__getattr__()`

异同：

- 都可以对实例属性进行获取拦截
- `__getattr__()` 适用于未定义的属性
- `__getattribute__()` 对所有属性的访问都会调用该方法

属性不在实例的 `__dict__` 中, `__getattr__` 被调用

### 属性描述符

描述符：实现特定协议的类

property 类需要实现 `__get__`、`__set__`、 `__delete__` 方法

property 的优点：

- 代码更简洁，可读性、可维护性更强。
- 更好的管理属性的访问。
- 控制属性访问权限，提高数据安全性。

```python
class Human(object):
    def __init__(self, name):
        self.name = name
        
    # 将方法封装成属性
    @property
    def gender(self):
        return 'M'
```

另一种property写法

```python
gender  = property(get_, set_, del_, 'other property')
```

被装饰函数建议使用相同的 gender2 

使用 setter 并不能真正意义上实现无法写入，gender被改名为 `_Article__gender`

```
class Human2(object):
    def __init__(self):
        self._gender = None
        # 将方法封装成属性
        @property
        def gender2(self):
            print(self._gender)
    
    # 支持修改
    @gender2.setter
    def gender2(self,value):
        self._gender = value
    
    # 支持删除
    @gender2.deleter
    def gender2(self):
        del self._gender

```


一个使用场景
```python
from sqlalchemy import Column, Integer, String, Float
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from manage import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)


# 使用装饰器完成password的读取和写入功能分离
    @property
    def password(self):
        return None
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
  
    def is_active(self):
        return True
```

## 新式类

新式类和经典类的区别：当前类或者父类继承了 object 类，那么该类便是新式类，否则便是经典类

### object 和 type 的关系
- object 和 type 都属于 type 类 (class 'type')
- type 类由 type 元类自身创建的。object 类是由元类 type 创建
- object 的父类为空，没有继承任何类
- type 的父类为 object 类 (class 'object')

`__class__` 查看由谁创建

`__bases` 查看继承关系

![image](0E45903A2E1E4AA88D6D1162D6CC168D)

## 类的继承

- 单一继承
- 多重继承
- 菱形继承（钻石继承）
- 继承机制 MRO
- MRO 的 C3 算法

### 菱形继承

```
# 钻石继承
class BaseClass(object):
    num_base_calls = 0
    def call_me(self):
        print ("Calling method on Base Class")
        self.num_base_calls += 1

class LeftSubclass(BaseClass):
    num_left_calls = 0
    def call_me(self):
        print ("Calling method on Left Subclass")
        self.num_left_calls += 1

class RightSubclass(object):
    num_right_calls = 0
    def call_me(self):
        print("Calling method on Right Subclass")
        self.num_right_calls += 1

class Subclass(LeftSubclass,RightSubclass):
    pass

a = Subclass()
a.call_me()
```
