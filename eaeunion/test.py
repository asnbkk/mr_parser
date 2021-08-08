keys = ['be_name', 
        'be_brief_name', 
        'be_type', 
        'country', 
        'reg_address', 
        'e_location', 
        'postal_address', 
        'phone', 
        'email']

values = [1, 2, 3, 4, 5, 6 , 7, 8, 9]

d = { keys[i]: values[i] for i in range(len(keys))}

print(d)