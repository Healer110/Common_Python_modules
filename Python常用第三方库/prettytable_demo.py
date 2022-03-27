#!/usr/bin/python
# -*-coding:utf-8 -*-
_author_ = 'Mr.Sun'
__date__ = '2022/3/20 22:11'

from prettytable import PrettyTable

tb = PrettyTable()
tb.field_names = ["City name", "Area", "Population", "Annual Rainfall"]
tb.add_row(["Adelaide",1295, 1158259, 600.5])
tb.add_row(["Brisbane",5905, 1857594, 1146.4])
tb.add_row(["Darwin", 112, 120900, 1714.7])
tb.add_row(["Hobart", 1357, 205556,619.5])

print(tb)
