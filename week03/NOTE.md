# 学习笔记

关于进程和线程的内容，以前的学习中涉及较少，但是通过老师的讲解，也感受到了掌握多线程编程的重要性。

自己目前在这一块基础比较薄弱，后续作针对训练。

## 进程和线程

进程是线程的集合，进程就是由一个或多个线程构成的，线程是操作系统进行运算调度的最小单位，是进程中的一个最小运行单元

## 多进程和多线程

### 多线程

多线程就是一个进程中同时执行多个线程

### 多线程适用场景

- IO 密集型任务

### Python 多线程的问题

由于 Python 中 GIL 的限制，导致不论是在单核还是多核条件下，在同一时刻只能运行一个线程，导致 Python 多线程无法发挥多核并行的优势。

GIL 全称为 Global Interpreter Lock，中文翻译为全局解释器锁，其最初设计是出于数据安全而考虑的。

在 Python 多线程下，每个线程的执行方式如下：

1. 获取 GIL
2. 执行对应线程的代码
3. 释放 GIL

在一个 Python 进程中，GIL 只有一个。这样就会导致，即使是多核条件下，一个 Python 进程下的多个线程，同一时刻也只能执行一个线程。

不过对于爬虫这种 IO 密集型任务来说，这个问题影响并不大。而对于计算密集型任务来说，由于 GIL 的存在，多线程总体的运行效率相比可能反而比单线程更低。

## 并发和并行

### 并发

并发，英文叫作 concurrency。它是指**同一时刻只能有一条指令执行**，但是多个线程的对应的指令被快速轮换地执行。比如一个处理器，它先执行线程 A 的指令一段时间，再执行线程 B 的指令一段时间，再切回到线程 A 执行一段时间。

由于处理器执行指令的速度和切换的速度非常非常快，人完全感知不到计算机在这个过程中有多个线程切换上下文执行的操作，这就使得宏观上看起来多个线程在同时运行。但微观上只是这个处理器在连续不断地在多个线程之间切换和执行，每个线程的执行一定会占用这个处理器一个时间片段，同一时刻，其实只有一个线程在执行。

### 并行

并行，英文叫作 parallel。它是指同一时刻，有多条指令在多个处理器上同时执行，并行必须要依赖于多个处理器。不论是从宏观上还是微观上，多个线程都是在同一时刻一起执行的。

并行只能在多处理器系统中存在，如果我们的计算机处理器只有一个核，那就不可能实现并行。而并发在单处理器和多处理器系统中都是可以存在的，因为仅靠一个核，就可以实现并发。
