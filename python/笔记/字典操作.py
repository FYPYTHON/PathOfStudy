# coding=utf-8

# 字典合并

l_p = {"python": 'py', 'c++':'cpp'}
l_j = {'java': 'java', 'golang': 'go'}

l_t = l_p | l_j
# print(l_t)

# 解包合并

t = {**l_p, **l_j}
# print(t)


# 字典生成式
m_keys = ['py', 'c', 'go']
m_values = ['python', 'c', 'golang']
d = {key: value for key, value in zip(m_keys, m_values)}
# print(d)

# k,v互换
data = {'py': 'python', 'c': 'c', 'go': 'golang'}
# 1
data_r = {v:k for k,v in data.items()}
# 2
data_z = dict(zip(data.values(), data.keys()))
# print(data_r, data_z)

# 排序
s = {'python': '3', 'c': '1', 'golang': '2'}
d_s = sorted(s.items(), key=lambda d:d[1])
print(d_s)