import features
import tree

def user_input():
   user_features = []
   pclass = input("   What is your socioeconomic status? ((U)pper, (M)iddle, (L)ower) >>> ")
   if pclass == "Upper" or pclass == "upper" or pclass == "U" or pclass == "u":
      pclass = 1
   elif pclass == "Middle" or pclass == "middle" or pclass == "M" or pclass == "m":
      pclass = 2
   elif pclass == "Lower" or pclass == "lower" or pclass == "L" or pclass == "l":
      pclass = 3
   user_features.append(pclass)
   sex = input("   What is your gender? ((M)ale, (F)emale) >>> ")
   if sex == "Male" or sex == "male" or sex == "M" or sex == "m":
      sex = 0
   elif sex == "Female" or sex == "female" or sex == "F" or sex == "f":
      sex = 1
   user_features.append(sex)
   age = int(input("   How old are you? >>> ")) * 1.0
   user_features.append(age)
   sibsp = int(input("   How many relatives would you have with you? (Siblings + Spouse) >>> "))
   user_features.append(sibsp)
   parch = int(input("   How many relatives would you have with you? (Parents + Children) >>> "))
   user_features.append(parch)
   embark_point = input("   Where would you like board the Titanic from? ((C)herbourg, (Q)ueenstown, (S)outhampton) >>> ")
   if embark_point == "Southampton" or embark_point == "southampton" or embark_point == "S" or embark_point == "s":
      embark_point = 0
   elif embark_point == "Cherbourg" or embark_point == "cherbourg" or embark_point == "C" or embark_point == "c":
      embark_point = 1
   elif embark_point == "Queenstown" or embark_point == "queenstown" or embark_point == "Q" or embark_point == "q":
      embark_point = 2
   user_features.append(embark_point)
   title = input("   What is your title? (Mr., Mrs., Miss., Master., Rev., Dr., Offcr., Capt.) >>> ")
   if title == "Mr." or title == "Mr":
      title = 0
   elif title == "Mrs." or title == "Mrs":
      title = 1
   elif title == "Miss." or title == "Miss":
      title = 2
   elif title == "Master." or title == "Master":
      title = 3
   elif title == "Rev." or title == "Rev":
      title = 4
   elif title == "Dr." or title == "Dr":
      title = 5
   elif title == "Offcr." or title == "Offcr":
      title = 6
   elif title == "Capt." or title == "Capt":
      title = 7
   user_features.append(title)
   family_size = sibsp + parch + 1
   user_features.append(family_size)
   if age <= 10.0:
      age_interval = 0
   elif age > 60.0:
      age_interval = 2
   else:
      age_interval = 1
   user_features.append(age_interval)
   deck = -1
   if pclass == 1:
      deck = ord(input("   Which deck would you want your cabin to be on? (a, b, c, d, e, f, g, t) >>> ")) - 97
      if deck > 6:
         deck = 7
      #print(deck)
   user_features.append(deck)
   print(user_features)
   return user_features


if __name__ == '__main__':
    print("Loading Decision Tree...")
    X, y = features.get_data()
    clf = tree.DecisionTreeClassifier(3,1)
    clf.fit(X,y)
    input_vector = user_input()
    survival = clf.predict(input_vector)
    if survival == 1:
        print("You will live.")
    else:
        print("You will die!")
