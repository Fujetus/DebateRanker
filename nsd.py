import pandas
df = pandas.read_csv('NSD.csv')
print(df)
arr = df.to_numpy()
num_rows, num_cols = arr.shape
ranking = " "
name1 = "Inta"
name2 = "Melendi"
for i in range(0,num_rows):

    if str(arr[i][1]).upper().find(name1.upper() + " & " + name2.upper()) != -1:
        ranking = str(arr[i][0])

#pass the ranking into the html
print(ranking)
