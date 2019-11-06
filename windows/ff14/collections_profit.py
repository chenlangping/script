#!/usr/bin/env python
# -- coding:utf-8 --

product_time = 50

cost = int(input("成本 = "))
gil_given_by_system = int(input("系统给的金币 = "))
white_gil = int(input("白票 = "))
stone = int(input("捌型石头价格 = "))

real_cost = cost-gil_given_by_system
profit_for_one_product = (stone/500)*white_gil - real_cost

print("花费 = ", real_cost)
print("搓一个 = ", profit_for_one_product)
print("一小时收益 = ", profit_for_one_product*(3600/product_time))
