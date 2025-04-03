
import pandas as pd
import string

# Создаем список букв английского алфавита
letters = list(string.ascii_lowercase)

count_of_dots = 7
digit_to_letter = {i + 1: letters[i] for i in range(count_of_dots)}
#         a      b       c     d     e      f      g
mat = [[10000, 4.0,   10000, 10000, 10000, 10000, 10000],
       [10000, 10000, 10000, 10000, 4.5  , 10000, 10000],
       [10000, 10000, 10000, 10000, 10000, 10000, 10000],
       [10000, 7.5  , 10000, 10000, 3.5  , 10000, 4.5  ],
       [6    , 10000, 3.5  , 10000, 10000, 6.5  , 10000],
       [10000, 10000, 10000, 10000, 10000, 10000, 10000],
       [10000, 10000, 10000, 10000, 0    , 10000, 10000]]

df = pd.DataFrame(mat, index=["a", "b", "c", "d", "e", "f", "g"], columns=["a", "b", "c", "d", "e", "f", "g"])
print(df)

l0 = [10000, 10000, 10000, 0, 10000, 10000, 10000]

lambd = pd.DataFrame(l0, index=["a", "b", "c", "d", "e", "f", "g"], columns=[0])
print(lambd)


flag = 5
counter = 0
print()
while flag:
       if flag == 0:
              break
       print(f"\033[34m>>>>>>>>>>>>>>>>>>>>релаксация при {counter+1} шаге\033[0m")
       pred = lambd[counter].tolist()
       tec = l0
       for i in range( count_of_dots):
              if i == 3:
                     tec[i] = 0
              else:
                     now = df[letters[i+1]].tolist()
                     print(f"x_{i+1} = {now}")
                     minimum = 10000
                     for j in range(count_of_dots):
                            if now[j] != 10000:
                                   minimum = min(pred[j] + now[j], pred[i], minimum)
                                   print(f"{j+1}_minimum = min({pred[j]} + {now[j]}; {pred[i]}) = {pred[j] + now[j]}")
                     print(minimum)
                     tec[i] = minimum
       lambd[counter+1] = tec
       print(lambd)
       counter += 1
       flag -= 1