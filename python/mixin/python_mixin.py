# coding=utf-8
"""
Mixin是一种设计模式、设计思想

并不是某个特定的class或者函数．

Java中的Mixin叫interface

Ruby中的Mixin叫Module

[2]优点:

1.mixin设计迷失可以在不对类的内容的修改前提下，扩展类的功能（添加父类）
2.更加方便的组织和维护不同的组建
3.可以根据开发需要任意调整功能
4.可以避免产生更多的类

缺点：
受继承关系限制，推荐只有两层的继承使用。

#－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－

#案例一[3]:
"""
class Role:
    def walk(self):
       print('走')
 
#---------------------------------------------------------------
class RunMixin:
    def run(self):
       print('跑')
 
class PromptSkillMixin:
    def use_prompt_skill(self):
       print('使用了一个瞬发技能')
 
class WalkExMixin:#覆盖Role中的功能，因为下面是最先继承,Role是最后继承
    def walk(self):
       print('疾走')
 
class RoleEx(WalkExMixin, PromptSkillMixin, RunMixin, Role):
 
    def marco(self):
       return [self.run, self.use_prompt_skill]
 
    def use_marco(self):
        print("---------------use_marco技术----------------")
        for action in self.marco():
            action()
        print("－－－－－－－－use_marco结束－－－－－－－－－－")
if __name__ == '__main__':
    r = RoleEx()
 
    r.use_marco()
    r.walk()
"""
实验结果:

---------------use_marco技术----------------
跑
使用了一个瞬发技能
－－－－－－－－use_marco结束－－－－－－－－－－－－－－－－－－
疾走
"""


