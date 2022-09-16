# coding=utf-8
from name_config import family_names, boys_given_words1, boys_given_words2, girls_given_words1, girls_given_words2

import random
filename = 'name.txt'
f = open(filename,'w')
f.write('----------百家姓-----------\n')
for i in range(1,101):
    one_name = random.choice(family_names)
#print(one_name)

    is_boy = random.randint(1,2)
    one_or_two = random.randint(1,2)

    if is_boy ==1:
        if one_or_two == 1:
            picked_name = random.choice(boys_given_words1)
            picked_name += random.choice(boys_given_words1)
        else:
            picked_name = random.choice(boys_given_words2)
    else:
        if one_or_two == 1:
            picked_name = random.choice(girls_given_words1)
        else:
            picked_name = random.choice(girls_given_words2)
#print(picked_name)
    full_name = one_name + picked_name
    print(full_name)
    f.write(full_name)
    f.write('\n')
f.close()
print("\n-\n-\n")