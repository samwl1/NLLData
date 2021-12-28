import pandas as pd
df = pd.DataFrame(columns=['Name', 'Age'])
df.loc[0] = ['Y. Es', 19]

print (contain_values)
contain_values['Name'] = 'N. O'
df[df['Name'].str.contains('Es')] = contain_values
print(df[df['Name'].str.contains('O')])