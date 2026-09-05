import json

with open("translations.json", "r", encoding="utf-8") as file:
    translations = json.load(file)

print("Choose your language:")
print("1. English")
print("2. Tamil")
print("3. Hindi")

choice = input("Enter your choice: ")

if choice == "1":
    language = "english"
elif choice == "2":
    language = "tamil"
elif choice == "3":
    language = "hindi"
else:
    print("Invalid choice")
    exit()

print("\n" + translations[language]["weather"])
print(translations[language]["temperature"])
print(translations[language]["rainfall"])
print(translations[language]["humidity"])
print(translations[language]["wind"])
print(translations[language]["forecast"])
print(translations[language]["today"])
print(translations[language]["tomorrow"])
print(translations[language]["high"])
print(translations[language]["low"])
print(translations[language]["alert"])
