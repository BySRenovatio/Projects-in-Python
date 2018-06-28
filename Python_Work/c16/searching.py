# Binary search

name_list = range(0,128)
key = 456;
lower_bound = 0
upper_bound = len(name_list)-1
found = False
while lower_bound <= upper_bound and not found:
    middle_pos = (lower_bound+upper_bound) // 2
    if name_list[middle_pos] < key:
        lower_bound = middle_pos + 1
    elif name_list[middle_pos] > key:
        upper_bound = middle_pos - 1
    else:
        found = True
 
if found:
    print("The name is at position", middle_pos)
else:
    print("The name was not in the list.")