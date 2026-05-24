# Making a Coffee Shop

print("Hello, welcome to Spidey Coffee Shop")

name = input("What is your name?\n")

if name == "Ben" or name == "Patricia" or name == "Loki":
    evil_status = input("Are you evil?\n")
    if evil_status == "Yes":
        print("You're not welcome here evil " + name + "!! Get out of here!")
        exit("Evil ones are not allowed.")
    else:
        print("Oh, so you're one of those good " + name + "s. Come on in!!\n\n")
else:
    print("Hello " + name + ", thank you so much for coming in today.\n\n")

menu = "1.Black Coffee\n" + "2.Cappuccino\n" + "3.Frappuccino\n" + "4.Espresso\n" + "5.Latte\n"

order = input(
    "So " + name + ", what would you like to have from our menu?\n" + "This is what we are serving today.\n" + menu)

additional = input("Would you like to have extra whipped cream in Latte?\n")
if additional == "Yes":
    price = 10

if order == "Black Coffee":
    price = 2
elif order == "Cappuccino":
    price = 10
elif order == "Frappuccino":
    price = 15
elif order == "Espresso":
    price = 5
elif order == "Latte":
    price = 8
    additional = input("Would you like to have extra whipped cream in Latte?\n")
if additional == "Yes":
    price = 10

else:
    print("Sorry, we don't serve that here.")
    price = 0
    exit()

quantity = input("Okay " + name + ", how many cup(s) of " + order + " do you want?\n")

print("Sounds great " + name + "!!, we'll get your " + quantity + " cup(s) of " + order + " in a moment.")

total = price * int(quantity)

print("And your total for " + quantity + " cup(s) of " + order + ", would be $" + str(total) + ".\n")

print("Thank you so much " + name + ", keep coming.")