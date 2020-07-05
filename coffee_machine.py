class Machine:

    def __init__(self, water=400, milk=540, beans=120, cups=9, money=550):
        self.water = water
        self.milk = milk
        self.beans = beans
        self.cups = cups
        self.money = money

    def status(self, req_water, req_milk, req_beans, req_cups, req_money):
        if self.water - req_water < 0:
            print("Sorry, not enough water!")
        elif self.milk - req_milk < 0:
            print("Sorry, not enough milk!")
        elif self.beans - req_beans < 0:
            print("Sorry, not enough beans!")
        elif self.cups - req_cups < 0:
            print("Sorry, not enough cups!")
        else:
            print("I have enough resources, making you a coffee!")
            self.water = self.water - req_water
            self.milk = self.milk - req_milk
            self.beans = self.beans - req_beans
            self.cups = self.cups - req_cups
            self.money = self.money + req_money

    def fill(self):
        add_water = int(input("Write how many ml of water do you want to add:"))
        add_milk = int(input("Write how many ml of milk do you want to add:"))
        add_beans = int(input("Write how grams of coffee do you want to add:"))
        add_cups = int(input("Write how disposable cups of coffee do you want to add:"))
        self.water = self.water + add_water
        self.milk = self.milk + add_milk
        self.beans = self.beans + add_beans
        self.cups = self.cups + add_cups

    def take(self):
        print(f'I gave you ${self.money}')
        self.money = 0

    def remaining(self):
        print("The coffee machine has:")
        print(f'{self.water} of water')
        print(f'{self.milk} of milk')
        print(f'{self.beans} of coffee beans')
        print(f'{self.cups} of disposable cups')
        print(f'${self.money} of money')


start = Machine()
while True:
    action = input("Write action (buy, fill, take, remaining, exit):\n")
    if action == "buy":
        name = input("\nWhat do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu:\n")
        if name == "1":
            start.status(250, 0, 16, 1, 4)
        elif name == "2":
            start.status(350, 75, 20, 1, 7)
        elif name == "3":
            start.status(200, 100, 12, 1, 6)
        elif name == "back":
            continue
    elif action == "fill":
        start.fill()
    elif action == "take":
        start.take()
    elif action == "remaining":
        start.remaining()
    elif action == "exit":
        quit()
