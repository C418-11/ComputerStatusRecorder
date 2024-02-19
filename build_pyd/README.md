# 如何制作你的功能

## 1.编写环境搭建

按照本项目根目录下的[`README.md (点击打开)`](../README.md)文件进行基础环境搭建。

为了后续编译你的代码 你需要额外安装以下库：

* _setuptools 69.0.3_
* _Cython 3.0.8_

## 2.编写代码

### 2.1 配置文件编辑

!!! 启动一次程序 使其自动生成配置文件。

在项目目录[`.configs (点击打开)`](../.configs)下找到[`OtherFeatures.yaml (点击打开)`](../.configs/OtherFeatures.yaml)文件。

你将看到默认的：

```yaml
HelloWorld: false
YourFeatureName: Is Enabled (true | false)

```

将`YourFeatureName`替换为你想要的名字，然后将`Is Enabled`的值改为`true`。

例：

```yaml
HelloWorld: True

```

#### 配置文件行为

如果在配置文件中找到键，且键的值`bool()`为`True`时， 加载器会尝试

``` python
import Features.{键名}
```

### 2.2 编写代码

#### 2.2.1 编写文件基础描述

在项目目录[`Features (点击打开)`](../Features)下新建一个py文件，命名为你刚刚取的名字。

接着上面的例子，你将新建一个名为[`HelloWorld.py (点击打开)`](../Features/HelloWorld.py)的文件。

为了使编译器正确地识别python版本，你最好在文件开头加上这条注释

```python
# cython: language_level = 3
```

在后续版本可能会用到的可选变量

```python
__author__ = "C418____11 <553515788@qq.com>"  # 此功能作者
__version__ = "0.0.1Dev"  # 此功能的版本
```

#### 2.2.2 编写GUI页面

接着上面的例子，你将向[`HelloWorld.py (点击打开)`](../Features/HelloWorld.py)中写入以下代码

``` python
from UI.ABC import AbcUI
from UI.RegisterUI import register
```

这导入了一个UI的基类和一个用于注册UI的函数。

接下来你应该继承这个基类，并重写其中的方法

``` python
class HelloWorld(AbcUI):
    # --- 必须继承的方法 ---
    
    # 加载器会在主体加载完成后调用这个方法
    def setupUi(self):
        ...
        
    # 加载器调用这个方法来获取主控件
    def getMainWidget(self):
        ...
    
    # 加载器将会调用这个方法, 并将返回值作为页面名称
    def getTagName(self):
        ...
    
    # --- 可选继承的方法 ---
    
    # 当父控件大小改变时, 会调用这个方法, 用于调整子控件大小
    def ReScale(self, x_scale: float, y_scale: float):
        ...
        
    # 返回的值越小 页面越靠前
    def priority():
        ...
        
```

具体要实现的方法请参考[`UI.ABC.py (点击打开)`](../UI/ABC.py)

当前例子的实现代码如下

``` python
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QTabWidget, QLabel, QWidget

class HelloWorld(AbcUI):
    def __init__(self, _parent: QTabWidget):
        # 当前版本这行不必要, 只是为了让PyCharm不爆黄
        super().__init__(_parent)

        self._parent = _parent
        self.widget: QWidget | None = None
        self.Label: QLabel | None = None
        self.base_size: QSize | None = None

    # 重写抽象类的方法, 实现具体功能
    # 加载器会在主体加载完成后调用这个方法
    def setupUi(self):
        self.widget = QWidget(self._parent)

        self.Label = QLabel(self.widget)
        self.Label.setText(("Hello World!\n" * 3)[:-1])

    # 加载器调用这个方法来获取主控件
    def getMainWidget(self):
        return self.widget

    # 加载器将会调用这个方法, 并将返回值作为页面名称
    def getTagName(self):
        return "Hello World Page"

    # 当父控件大小改变时, 会调用这个方法, 用于调整子控件大小
    def ReScale(self, x_scale: float, y_scale: float):

        x = (self._parent.width() - self.Label.width()) // 2
        y = (self._parent.height() - self.Label.height()) // 2

        # 将Label居中
        self.Label.move(
            x,
            y,
        )
    
    # 返回的值越小 页面越靠前
    @staticmethod
    def priority():
        return float("-inf")
```

为了让`HelloWorld`类能够被加载器加载，需要将其注册：

``` python
# 将这个类注册到界面加载器中
register(HelloWorld)
```

现在这个文件应该像这样： [`HelloWorld.py (点击打开)`](../Features/HelloWorld.py)

```python
# -*- coding: utf-8 -*-
# cython: language_level = 3

__author__ = "C418____11 <553515788@qq.com>"
__version__ = "0.0.1Dev"

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QTabWidget, QLabel, QWidget

# 导入抽象类，用于继承
from UI.ABC import AbcUI
from UI.RegisterUI import register


# 继承抽象类，实现具体功能
class HelloWorld(AbcUI):
    def __init__(self, _parent: QTabWidget):
        # 当前版本这行不必要, 只是为了让PyCharm不爆黄
        super().__init__(_parent)

        self._parent = _parent
        self.widget: QWidget | None = None
        self.Label: QLabel | None = None
        self.base_size: QSize | None = None

    # 重写抽象类的方法, 实现具体功能
    # 加载器会在主体加载完成后调用这个方法
    def setupUi(self):
        self.widget = QWidget(self._parent)

        self.Label = QLabel(self.widget)
        self.Label.setText(("Hello World!\n" * 3)[:-1])

    # 加载器调用这个方法来获取主控件
    def getMainWidget(self):
        return self.widget

    # 加载器将会调用这个方法, 并将返回值作为页面名称
    def getTagName(self):
        return "Hello World Page"

    # 当父控件大小改变时, 会调用这个方法, 用于调整子控件大小
    def ReScale(self, x_scale: float, y_scale: float):
        x = (self._parent.width() - self.Label.width()) // 2
        y = (self._parent.height() - self.Label.height()) // 2

        # 将Label居中
        self.Label.move(
            x,
            y,
        )

    # 返回的值越小 页面越靠前
    @staticmethod
    def priority():
        return float("-inf")


# 将这个类注册到界面加载器中
register(HelloWorld)
```

#### 2.2.3 编写Menu

* 参考[`Opacity.py (点击打开)`](../DefaultFeatures/Opacity.py)
* 参考[`WindowTop.py (点击打开)`](../DefaultFeatures/WindowTop.py)

## 3. 测试

接着上面的例子

* 确保你编写的功能处于启用状态[`OtherFeatures.yaml (点击打开)`](../.configs/OtherFeatures.yaml)
* 从程序入口[`main.py (点击打开)`](../main.py)启动程序 ```python ../main.py```

## 4. 编译

确保你所有额外的依赖项都在[`Features (点击打开)`](../Features)目录下并且能被正确导入

打开[`setup.py(点击打开)`](setup.py)并执行```python setup.py```

你应该会看见如下输出

``` text
1: Pyd Default Features, 2: Pyd Other Features, 3: Print Depends, 4: Exit
```

输入 `2` 将会开始编译并将结果保存到 [`./Build/pyd/OtherFeatures (点击打开)`](./Build/pyd/OtherFeatures)目录下

如果文件树丢失， 需按照源.py文件的文件树为.pyd文件创建文件树

将新创建的pyd文件树放入从发布包中解压的文件树中的/_internal/Features目录下

``` text
解压后的文件树：
.
├── StatusRecorder.exe
└── _internal
    ├── DefaultFeatures
    │   ├── NetWorkTraffic.pyd
    │   └── Opacity.pyd
    └── Features
        ├── HelloWord.pyd
        └── 你新创建的文件树
```
