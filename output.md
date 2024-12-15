# 表单设计器实现原理

Back to document

首先，wflow的表单是通过json动态渲染出来的，表单设计器生成的也是json，并非是生成代码，该json存储在 wflow\_model\_historys 和 wflow\_models表的 form\_items字段

表单渲染实现原理来源于vue的动态组件 <components is="表单组件名称"></components>

利用此特性，我们可以通过一个字符串，动态显示成一个vue组件

例如：有如下json

​

示例表单渲染json

JavaScript

Copy

99

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

\[\
\
{\
\
id:"field454894798",\
\
name:"TextInput",//表单组件名称\
\
title:"文本输入框",\
\
props:{\
\
//表单组件的自定义props配置项\
\
}\
\
},\
\
{\
\
id:"field45888888",\
\
name:"NumberInput",//表单组件名称\
\
title:"数字输入框",\
\
props:{\
\
//表单组件的自定义props配置项\
\
}\
\
}\
\
\]

那么我们可以使用定义如下表单组件，对其进行动态渲染

​

FormRender.vue 简单示例

Vue

Copy

99

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

<template>

<el-form:model="formData">

<el-form-item:label="cp.title":prop="cp.id"v-for="cp in formJson":key="cp.id">

<componentsv-model="formData\[cp.id\]":is="cp.name"v-bind="cp.props"/>

</el-form-item>

</el-form>

</template>

<script>

//这两个组件自己定义就好了

importTextInputfrom'../TextInput.vue'

importNumberInputfrom"./NumberInput.vue";

exportdefault{

name:"FormRender",

props:{},

data(){

return{

formData:{},

formJson:\[\]//表单json

}

}

}

这样子，表单就渲染出来了，并且可以绑定表单值。理解原理就知道表单怎么搞了，复杂的组件自己再尝试扩充。

​

1 like

- ![语雀用户-YW1e3t](https://mdn.alipayobjects.com/huamei_0prmtq/afts/img/A*khrYRYi6VN0AAAAAAAAAAAAADvuFAQ/original)

1

[旅人](https://wflow.yuque.com/lvren-ybpix)

05-23 02:54

1782

IP region江西

Report

Markup comments (0)

Sign Up / Login Yuque to comment

[![](https://cdn.nlark.com/yuque/0/2024/png/2819278/1710810486051-avatar/6ed8d9fb-6745-48e2-b334-e8aa5503c947.png?x-oss-process=image%2Fresize%2Cm_fill%2Cw_32%2Ch_32%2Fformat%2Cpng)](https://wflow.yuque.com/dashboard)

wflow-pro