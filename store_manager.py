#Keenan Githu
#Final Project
#December 4, 2024
#SE116.02

#PROGRAM PROMPT: 
"""
Build a store management program/game. The program will allow the user to
have multiple options when it comes to upgrading the store and its contents.
The game will be randomized in some scenarios, which will make each playthrough 
unique to one another. There will be 30 days to build a store before your store is inspected. If you pass, you win
the game, and can continue to keep playing for as long as you like (or until the game breaks). If you fail,
you'll lose the game, and will have to start back from scratch.
"""

#VARIABLE DICTIONARY:
"""
"""

#Notes:
"""
THIS PART OF DOCUMENTATION IS FOR THINGS NOT FULLY EXPLAINED IN THE CODE, AND IS STATED EXPLICITLY IN THE ASSOCIATED SECTION
TO GO HERE FOR A BETTER IDEA ON HOW CERTAIN FEATURES WORK.

EVENTS_DICT:
Each event in the game is chosen from random. The elements in the lists are grouped in twos, with the
first element being the event title, and the second element being the modifier to an associated value.

Take for example ('Petty Theft', 0.98) under 'Convenience Store'. The title of the event is petty theft, and the 
money total is multiplied by 0.98 to get a 2% decrease in money. 

The third pair in each list is a modifier to employee count. It is always counted as losing 1 employee, regardless of store type.

The final pair is technically a trio, as it always adds 2 to the employee count (if the prompt is accepted) and
a percentage of money to the overall money total.

These events are ordered so it's possible to use the same code for all store variations. The first three are always negative, while the
latter three are always positive.


EVENTS:
Every 5th game day, excluding day 5 itself, the game will roll for a random event to happen.
Each event has a different percentage chance of it happening. Below will define each chance of something happening:

Theft/Vandalism: 12%
Lost/Damaged: 18%
Lose Employee: 10%
Local Reviews: 20%
Popular Product: 30%
Competition Shutdown: 10%

The rolling system is heavily biased towards positive events, 60% of the time will be positive. 

Out of all possibility, the lowest ones are Competition Shutdown and Lose Employee. Competition Shutdown is
obviously low: it gives the user significant advantage, especially on something like Hardware Store, which gives them
30% more Cash. Lose Employee, on the other hand, will increase the Stress of other employees the most out of any upgrades,
adding an additional 3 points onto Stress.


EMPLOYEE QUITTING MATH:
I chose to use exponential growth, since it was the easiest to implement. Below is a list for all numbers that the variable quit_math can be:
1: 1%
2: 2%
3: 3%
4: 5%
5: 6%
6: 7%
7: 9%
8: 10%
9: 12%
10: 13%
11: 15%
12: 17%
13: 19%
14: 21%
15: 23%
16: 26%

The chances don't get too extreme until about 11 stress, but this is rolled daily. The idea of it is that you don't need to hire more employees, as long as you keep
them happy by upgrading things related to it.
"""




#for randomization
import random

#timing stuff
from time import sleep

#some fun clear screen stuff
from os import system, name

#I've used the same segment to try and switch a variable type so many times, I'm making a function for it
#I think this is the only function with parameters, even then, it's only one.
def tryToConvert(converting):
    try:
        converting = int(converting)
    except:
        invalid_message()
    return converting

#rolling for an event
def checkForEvent():
    global stress
    print("\nEvent:")

    #every 5th day and not on the 30th
    if day_count % 5 == 0 and day_count != 30:
        random_event = random.randint(1,1000)

        if random_event <= 120:
            #theft/vandalism
            print(store_events[store_selection][0])
            print(f"\n{store_events_messages[store_selection][0]}")
            store_statistics['Money'] = store_statistics['Money'] * store_events[store_selection][1]
            sleep(0.1)
            print(store_events_messages[store_selection][1])

        elif random_event >= 121 and random_event <= 300:
            #lost/damaged
            print(store_events[store_selection][2])
            print(f"\n{store_events_messages[store_selection][2]}")
            store_statistics['Money'] = store_statistics['Money'] * store_events[store_selection][3]
            sleep(0.1)
            print(store_events_messages[store_selection][3])

        elif random_event >= 301 and random_event <= 400:
            #employee injured
            stress += 3
            print(store_events[store_selection][4])
            print("+3 Stress")
            print(f"\n{store_events_messages[store_selection][4]}")
            store_statistics['Employees'] -= 1
            sleep(0.1)
            print(store_events_messages[store_selection][5])

        elif random_event >= 401 and random_event <= 600:
            #local reviews
            print(store_events[store_selection][6])
            print(f"\n{store_events_messages[store_selection][6]}")
            store_statistics['Money'] = store_statistics['Money'] * store_events[store_selection][7]
            sleep(0.1)
            print(store_events_messages[store_selection][7])

        elif random_event >= 601 and random_event <= 900:
            #popular product
            print(store_events[store_selection][8])
            print(f"\n{store_events_messages[store_selection][8]}")

            if store_selection == 'Book Store':
                book_store_money_math = round((random.randint(10,15))/10, 2)
                store_statistics['Money'] *= book_store_money_math
                print("...")
                sleep(0.5)
                print(f"\nYou got {(((book_store_money_math)*100)-100):.0f}% more money!")

            else:
                store_statistics['Money'] = store_statistics['Money'] * store_events[store_selection][9]

            sleep(0.1)
            print(store_events_messages[store_selection][9])

        else:
            #competitor down/hired by city
            print(store_events[store_selection][10])
            print(f"\n{store_events_messages[store_selection][10]}")
            store_statistics['Money'] = store_statistics['Money'] * store_events[store_selection][12]

            if store_selection != 'Hardware Store':
                hire_competitor = input("Would you like to hire your competitors employees? [y/n]: ").lower()

                while hire_competitor != 'y' and hire_competitor != 'n':
                    invalid_message()
                    hire_competitor = input("Would you like to hire your competitors employees? [y/n]: ").lower()

                if hire_competitor == 'y':
                    store_statistics['Employees'] += 2

            sleep(0.1)
            print(store_events_messages[store_selection][12])
    else:
        print("None.")

#add product option
def addProduct():

    #condition to start loop
    proceed_with_new_product = 'y'
    while proceed_with_new_product == 'y':

        #placeholder variables, so there isn't too many input statements
        new_product_price = 'a'
        new_product_quantity = 'a'

        #random costs change with store selection
        #Grocery Store rolls $1 to $20
        if store_selection == 'Grocery Store':
            new_random_cost = (random.randint(100,2000)/100)
        
        #Convenience Store rolls $1 to $9
        elif store_selection == 'Convenience Store':
            new_random_cost = (random.randint(100, 900)/100)
        
        #Book Store rolls $5 to $25
        elif store_selection == 'Book Store':
            new_random_cost = (random.randint(500, 2500)/100)
        
        #Electronics Store rolls $15 to $120
        elif store_selection == 'Electronics Store':
            new_random_cost = (random.randint(1500, 12000)/100)
        
        #Hardware Store rolls $6 to $140
        elif store_selection == 'Hardware Store':
            new_random_cost = (random.randint(600, 14000)/100)

        #asks for the product they want to sell at their store
        new_product = input("Enter the name of the product you want to buy: ")

        #ends the purchasing loop if there's at least 3 products in the store
        if new_product == 'end' or new_product == 'End' or new_product == 'END':
            if len(store_statistics['Products']) < 3:
                print("You need to have at least 3 products for your store.")
                continue
            else:
                proceed_with_new_product = 'n'
                continue

        #checks if new_product_quantity is an integer continuously
        while type(new_product_quantity) != int:
            new_product_quantity = input(f"Enter how much {new_product} you want to buy: ")
            new_product_quantity = tryToConvert(new_product_quantity)
            continue

        cost_for_new_product = new_product_quantity * new_random_cost

        print(f"\n\nMoney: ${store_statistics['Money']:.2f}\n\n")
        print(f"This amount of {new_product} will cost ${cost_for_new_product:.2f} at ${new_random_cost:.2f} per item.")

        #placeholder value, not at the top because of an oversight
        proceed_with_new_product = 'b'

        #checks if the user wants to add this product
        while proceed_with_new_product != 'y' and proceed_with_new_product != 'n':
            proceed_with_new_product = input("Would you like to buy this new product for your store? [y/n]: ")
            if proceed_with_new_product != 'y' and proceed_with_new_product != 'n':
                invalid_message()
        
        #if the prompt is denied, make proceed_with_new_product yes and continue
        #Yes, this was an oversight while designing
        if proceed_with_new_product == 'n':
            proceed_with_new_product = 'y'
            continue
        #if you can't afford it
        if store_statistics['Money'] - cost_for_new_product < 0:
            print("\nYou do not have enough money to purchase this product.\n\n")
            continue
        
        #take money from total
        store_statistics['Money'] -= cost_for_new_product

        #print it
        print(f"\n\nMoney: ${store_statistics['Money']:.2f}\n\n")

        while type(new_product_price) != float:
            new_product_price = input(f"Enter the price that {new_product} will have: $")
            try:
                new_product_price = float(new_product_price)
            except:
                invalid_message()
                continue

        
        if new_product not in store_statistics['Products']:
            store_statistics['Products'].append(new_product)
            store_statistics['Product Quantities'].append(new_product_quantity)
            store_statistics['Product Prices'].append(new_product_price)
            store_statistics['Product Costs'].append(new_random_cost)
            store_statistics['Product Original Costs'].append(new_product)
            store_statistics['Product Original Costs'].append(new_random_cost)
        else:
            store_statistics['Product Quantities'][store_statistics['Products'].index(new_product)] += new_product_quantity
            store_statistics['Product Prices'][store_statistics['Products'].index(new_product)] = new_product_price
            store_statistics['Product Costs'][store_statistics['Products'].index(new_product)] = new_random_cost
            store_statistics['Product Original Costs'][store_statistics['Products'].index(new_product)] = new_random_cost
    

        print(f"Your order of {new_product_quantity} {new_product} will be delivered tomorrow!\n\n")
        sleep(1)





#hiring employees option
def hireEmployees():
    global stress
    global hire_employee
    print(f"\nAttempting to hire employees...")
    sleep(2)

    #25% chance to hire a new employee, can only be used once a day
    if hire_employee == True:
        hire_check = random.randint(1,4)
        if hire_check == 1:
            print("\nSuccessfully found a new employee! They start tomorrow!\n\n")
            if stress > 0:
                if stress > 1:
                    stress -= 2
                else:
                    stress -= 1

        else:
            print("\nNo new employees found. Better luck tomorrow.\n\n")
    else:
        print("You've already tried to hire someone today. Try again tomorrow.")
    
    #wont let them hire again today
    hire_employee = False

#store upgrades option
def storeUpgrades():
    global first_event_prevention
    global second_event_prevention
    global parking_lot
    global advertisement
    global store_size

    upgrading = True
    while upgrading == True:

        #a variable so i can have a clean while loop
        upgrade_selection = ''
        random_count_variable = 2

        print("Upgrade:\t\tCost:")

        #prints the upgrades so they're in-line with the associated tags
        print(f"1. {store_upgrade_options[store_selection][0]}\t\t${store_upgrade_options[store_selection][1]}")
        print(f"2. {store_upgrade_options[store_selection][2]}\t${store_upgrade_options[store_selection][3]}")

        #weird loop so it properly displays all options
        for i in range(1,6,2):

            #counting variable with a name I hopefully won't use again
            random_count_variable += 1

            #Store Size is annoying
            if random_count_variable == 3:
                print(f"{random_count_variable}. {store_upgrade_options['All Stores'][i-1]}\t\t${store_upgrade_options['All Stores'][i]}")

            else:
                #prints the upgrade so it's in-line with others
                print(f"{random_count_variable}. {store_upgrade_options['All Stores'][i-1]}\t${store_upgrade_options['All Stores'][i]}")

        print("6. Go Back")
        #not an integer by default, will loop upgrade_selection until it is
        while (type(upgrade_selection) != int) or upgrade_selection < 1 or upgrade_selection > 6:
            upgrade_selection = input("Enter the upgrade you'd like to get [1-6]: ")
            upgrade_selection = tryToConvert(upgrade_selection)
            continue

        #if they already have the first or second upgrade, will prevent them from buying it again
        if upgrade_selection == 1 and first_event_prevention == True:
            print("You've already gotten that upgrade!\n")
            continue

        if upgrade_selection == 2 and second_event_prevention == True:
            print("You've already gotten that upgrade!\n")
            continue

        #this runs if the user has enough money to buy the associated upgrades
        if upgrade_selection == 1 and store_statistics['Money'] - store_upgrade_options[store_selection][1] >= 0:
            print("Upgrade acquired! Your store is safer than ever!\n")
            first_event_prevention = True

        #same as above, but with the rest of the upgrades
        elif upgrade_selection == 2 and store_statistics['Money'] - store_upgrade_options[store_selection][3] >= 0:
            print("Upgrade acquired! Your products will come in greater shape than ever!\n")
            second_event_prevention = True

        elif upgrade_selection == 3 and store_statistics['Money'] - store_upgrade_options["All Stores"][1] >= 0:
            print("Upgrade acquired! Your store grows ever-bigger, and can now bring more people every day! (additive upgrade)\n")
            store_size += 1
            store_statistics['Daily People'] += store_statistics['Daily People']

        elif upgrade_selection == 4 and store_statistics['Money'] - store_upgrade_options["All Stores"][3] >= 0:
            print("Upgrade acquired! Your parking lot draws more people in, and more people are buying! (multiplicative upgrade)\n")
            parking_lot += 1
            store_statistics['Daily People'] = round(store_statistics['Daily People'] * (1+(parking_lot/20)))

        elif upgrade_selection == 5 and store_statistics['Money'] - store_upgrade_options["All Stores"][5] >= 0:
            print("Upgrade acquired! Your store is now more well-known, and will bring in more people! (multiplicative upgrade)\n")
            advertisement += 1
            store_statistics['Daily People'] = round(store_statistics['Daily People'] * (1+(advertisement/10)) )
        
        elif upgrade_selection == 6:
            upgrading = False
            continue

        #if they cant afford any of the upgrades
        else:
            print("You have insufficient funds for that upgrade.")
        

#manage employees option
def manageEmployees():
    #globals and variable set up
    global cleanliness_rating
    global stress
    global employee_training

    manage_employee_options = ''
    training_check = ''
    cleaining_check = ''
    proceed_with_firing = ''

    #print options
    print(f"\n1. Employee Training {employee_training}")
    print("2. Store Cleaning")
    print("3. Let Go Of Employee")
    print("4. Go Back")

    while (type(manage_employee_options) != int) or manage_employee_options < 1 or manage_employee_options > 4:
        manage_employee_options = input("Enter an option from the list above [1-3]: ")
        manage_employee_options = tryToConvert(manage_employee_options)
        continue

    #employee training
    if manage_employee_options == 1:
        print(f"\n\nMoney: ${store_statistics['Money']:.2f}\n\n")
        print("A new training program for your employees to do.")

        #while loop to double check
        while training_check != 'y' and training_check != 'n':
            training_check = input(f"Employee Training will cost ${employee_training*800}. Would you like to continue? [y/n]: ")
            if training_check != 'y' and training_check != 'n':
                invalid_message()
                continue

        #user agrees and has enough money
        if store_statistics['Money'] - (employee_training*800) >= 0 and training_check == 'y':
            print("Employees have now received better training. Stress reduced by 1.")
            store_statistics['Money'] - (employee_training*800)
            stress -= 1
            employee_training += 1

        #user agrees but doesn't have enough
        elif store_statistics['Money'] - (employee_training*800) < 0 and training_check == 'y':
            print("You don't have enough to afford better training.")

    #store cleaning
    if manage_employee_options == 2:
        print(f"\n\nMoney: ${store_statistics['Money']:.2f}\n\n")
        print("You offer some employees overtime pay to clean the store.")

        #while loop to double check
        while cleaining_check != 'y' and cleaining_check != 'n':
            cleaining_check = input("Cleaning the store thoroughly will cost you $600. Would you like to continue? [y/n]: ")
            if cleaining_check != 'y' and cleaining_check != 'n':
                invalid_message()
                continue

        #user agrees and they have enough money
        if store_statistics['Money'] - 600 >= 0 and cleaining_check == 'y':
            if cleanliness_rating != 'A':
                print("Your store is now in much better shape than before!")
                cleanliness_rating = alphabet_list.index(cleanliness_rating-1)
                store_statistics['Money'] - 600
            else:
                print("Your store is already spotless!")

        #user agrees but doesn't have enough
        elif store_statistics['Money'] - 600 < 0 and cleaining_check == 'y':
            print("You cannot afford to pay for overtime cleaning.")

    #firing employee
    if manage_employee_options == 3:
        print("This will remove an employee, which will lessen the amount of money towards wages.")
        print("However, this will also increase stress by 2.")

        #while loop to double check
        while proceed_with_firing != 'y' and proceed_with_firing != 'n':
            cleaining_check = input("Cleaning the store thoroughly will cost you $600. Would you like to continue? [y/n]: ")
            if proceed_with_firing != 'y' and proceed_with_firing != 'n':
                invalid_message()
                continue

        #employee gets fired
        if proceed_with_firing == 'y':
            print("An employee has been let go. Stress has increased by 2.")
            stress += 2
            store_statistics['Employees'] -= 1
    
    #go back
    if manage_employee_options == 4:
        print("Going Back...\n")

def checkInventory():
    #variable for looping
    check_inventory_loop = 'y'

    #loop
    while check_inventory_loop == 'y':
        price_change = ''
        accept_sell = ''
        check_inventory_options = ''

        #reprint the product information
        print("Products:\t\tPrice:\t\tQuantity:")
        for x in range(len(store_statistics['Products'])):
            print(f"{store_statistics['Products'][x]}\t\t\t${store_statistics['Product Prices'][x]:.2f}\t\t{store_statistics['Product Quantities'][x]}")
        
        print(f"\n1. Sell Products")
        print(f"2. Change Price of Item")
        print("3. Go Back\n")

        #check_inventory_options is a string by default, loops until it isnt
        while (type(check_inventory_options) != int) or check_inventory_options < 1 or check_inventory_options > 3:
            check_inventory_options = input("Enter a number from the list above [1-3]: ")
            check_inventory_options = tryToConvert(check_inventory_options)
        
        #sell products
        if check_inventory_options == 1:

            #used for item name input, the point being that no one will enter this as an actual item name, so the loop looks better
            sell_item_check = 'efwewrg8429tg9n4589gh2pb5uobv3467vb4tuivb49785b3ubfo9234bfd234buf9843hbobfeoubg3 jirv ber 234bf23bo'

            #the first sell_item_check is nearly impossible to appear in the products list
            while sell_item_check not in store_statistics['Products']:
                sell_item_check = input("\nWhich product would you like to get rid of? (caps sensitive): ")
                if sell_item_check not in store_statistics['Products']:
                    invalid_message()
                    continue
            
            #prints the item the user is trying to sell
            print(f"You are trying to sell {store_statistics['Product Quantities'][store_statistics['Products'].index(sell_item_check)]} {sell_item_check} purchased at ${store_statistics['Product Original Costs'][(store_statistics['Products'].index(sell_item_check))+1]:.2f}")

            #refer to variable name
            better_looking_original_price = round(store_statistics['Product Original Costs'][(store_statistics['Products'].index(sell_item_check))+1])
            sell_offer = (random.randint(100, better_looking_original_price*100))/100

            #accept_sell is already neither therefore it will keep looping until it is either
            while accept_sell != 'y' and accept_sell != 'n':
                accept_sell = input(f"Another company has offered {sell_offer} per unit to buy all of your {sell_item_check}. Would you like to accept this offer? [y/n]: ")
                if accept_sell != 'y' and accept_sell != 'n':
                    invalid_message()
                    continue
            
            #if they choose yes...
            if accept_sell == 'y':
                #money is updated, multiplying the quantity by the sell offer and adding to the Money
                store_statistics['Money'] += store_statistics['Product Quantities'][store_statistics['Products'].index(sell_item_check)] * sell_offer

                #the item is popped from quantity list
                store_statistics['Product Quantities'].pop([store_statistics['Products'].index(sell_item_check)])

                #the item is popped from the price list
                store_statistics['Product Prices'].pop([store_statistics['Products'].index(sell_item_check)])

                #the item is removed from the product list
                store_statistics['Products'].remove(sell_item_check)
        
        #price changing
        if check_inventory_options == 2:
            #random string that won't be in any product list
            price_change_check = 'efwewrg8429tg9n4589gh2pb5uobv3467vb4tuivb49785b3ubfo9234bfd234buf9843hbobfeoubg3 jirv ber 234bf23bo'
            
            #price_change_check isn't in Products by default
            while price_change_check not in store_statistics['Products']:
                price_change_check = input("What item would you like to change the price of? (caps sensitive): ")
                if price_change_check not in store_statistics['Products']:
                    invalid_message()
                    continue
            
            #the longest single line of code in this program
            #it prints the item the user is trying to sell
            print(f"You are trying to change the price of {store_statistics['Product Quantities'][store_statistics['Products'].index(price_change_check)]} {price_change_check} purchased at ${store_statistics['Product Original Costs'][store_statistics['Product Original Costs'].index(price_change_check)+1]:.2f} and currently selling for ${store_statistics['Product Prices'][store_statistics['Products'].index(price_change_check)]:.2f}")

            #price_change isnt a float by default, will not stop until is
            while type(price_change) != float:
                price_change = input("What do you want to change the price to?: $")
                try:
                    price_change = float(price_change)
                except:
                    invalid_message()
                    continue
            
            #changes the price to its new value
            store_statistics['Product Prices'][store_statistics['Products'].index(price_change_check)] = price_change
        
        #go back
        if check_inventory_options == 3:
            check_inventory_loop = 'n'
            continue


#customer generation for each day
def customerGenerator():

    #how many times the sales is rolled is based off of the amount of people
    daily_people = store_statistics['Daily People']

    #initializing the comparison stuff
    total_price_comparison = 0
    price_comparison = []

    #runs for each item in Product Costs, a list that stores the cost of each item (not selling price)
    for i in range(len(store_statistics['Product Costs'])):

        #this is a variation of SMAPE (Symmetric mean absolute percentage error) I found on Google. Is it overly complicated for something like this? Yes. Does it work? Also yes.
        #1. The original cost of the product is subtracted from the selling price (from now on, known as A)
        #2. The original cost of the product is added to the selling price (from now on, known as B)
        #3. B is then divided by 2 (still referred to as B)
        #4. A is then divided by B (from now on, known as C)
        #5. C is then multiplied by 100, before being divided by 2 (still C)
        #6. C is then multiplied by -1 to make it positive

        #the higher the output is, the less it will sell, due to the price difference between original cost and selling price
        comparison = round(((((store_statistics['Product Costs'][i]-store_statistics['Product Prices'][i])/((store_statistics['Product Costs'][i]+store_statistics['Product Prices'][i])/2)) * 100)/2)*-1)

        #added to the price comparison list
        price_comparison.append(comparison)

        #added together with total_price_comparison
        total_price_comparison += comparison

    #loops through each customer and their selections
    while daily_people > 0:
        
        #just loop stuff
        daily_people -= 1
        
        #list of items that determines which ones sell, and how many of them
        sell = []

        #random number based off of the total comparison number
        random_purchase = random.randint(1, total_price_comparison)

        #loops through the price_comparison list. This could've been the majority of lists in the program, but this one is local.
        for i in range(len(price_comparison)):
            #subtract the comparison from the total_price_comparison
            #greater than is so that numbers with higher values dont sell as well
            if total_price_comparison - price_comparison[i] > random_purchase:
                #random number that will be sold
                sell_quantity = random.randint(1,3)
                #add it to the sell list
                sell.append(sell_quantity)
            
            #replaces the value in that slot with a zero
            else:
                sell.append(0)

        #another loop for selling products
        for i in range(len(sell)):
            #if the product is actually being sold
            if sell[i] > 0:
                #making sure we aren't selling ghost items
                if store_statistics['Product Quantities'][i] - sell[i] < 0:
                    continue
                #if we aren't selling ghost items
                else:
                    store_statistics['Product Quantities'][i] -= sell[i]
                #adding money to the bank
                store_statistics['Money'] = store_statistics['Money'] + (sell[i] * store_statistics['Product Prices'][i])




    

        



def options_list():
    print("---Store Manager---")
    print("-------------------")
    sleep(0.1)
    print("1. Buy Products")
    sleep(0.1)
    print("2. Hire Employees")
    sleep(0.1)
    print("3. Store Upgrades")
    sleep(0.1)
    print("4. Manage Employees")
    sleep(0.1)
    print("5. Manage Inventory")
    sleep(0.1)
    print("6. End Day")
    sleep(0.1)

def clear():
    if name == 'nt': #for windows
        _ = system('cls')
    else: #for mac and linux
        _ = system('clear')

#invalid message printer
def invalid_message():
    print("\n\t***Invalid Input***\n")

#assigning initial variables so I don't have to put 2 input statements later on
store_selection = 0
store_name = ''
Game = True
day_count = 0
stress = 0
cleanliness_rating = 'A'
alphabet = 'ABCDEF'
alphabet_list = list(alphabet)

#variables for store upgrades
first_event_prevention = False
second_event_prevention = False
hire_employee = True
store_size = 1
parking_lot = 1
advertisement = 0

#variables for employee management
employee_training = 1

#dictionary to get the store list from
store_types = {
    '1': 'Grocery Store',
    '2': 'Convenience Store',
    '3': 'Book Store',
    '4': 'Electronics Store',
    '5': 'Hardware Store'
}

store_upgrade_options = {
    'Grocery Store': ['Safer Snacks', 4000, 'Transport Training', 3000],
    'Convenience Store': ['SECURITY', 500, 'Transport Training', 1800],
    'Book Store': ['SECURITY', 2000, 'Transport Training', 1800],
    'Electronics Store': ['SECURITY', 3500, 'Transport Training', 2500],
    'Hardware Store': ['SECURITY', 4500, 'Transport Training', 3000],
    'All Stores': [f'Store Size {store_size+1}', 1200*(store_size+1), f'Parking Lot {parking_lot+1}', 1500*(parking_lot+1), f'Advertisement {advertisement+1}', 3000*(advertisement+1)]
}

#starting values each store gets, first list element is money, second is the number of employees
store_starting_stuff = {
    'Grocery Store': [15000, 16, 20],
    'Convenience Store': [5000, 5, 9],
    'Book Store': [8000, 10, 10],
    'Electronics Store': [12000, 8, 20],
    'Hardware Store': [18000, 12, 10]
}

#events that will periodically occur throughout the game, see NOTES, under EVENTS_DICT
store_events = {
    'Grocery Store': ['Produce Gone Bad', 0.8, 'Lost In Shipment', 0.9, 'Work Accident', 1, 'Local Reviews', 1.1, 'I Got Here First!', 1.2, 'Competitor Shutdown', 2, 1.2],
    'Convenience Store': ['Petty Theft', 0.98, 'Lost In Shipment', 0.9, 'Employee Down', 1, 'Local Reviews', 1.05, 'I Got Here First!', 1.1, 'Competitor Shutdown', 2, 1.1],
    'Book Store': ['Mild Property Destruction', 0.95, 'Lost In Shipment', 0.9, 'Shelf Collapse', 1, 'Local Reviews', 1.1, 'Pen In My Pocket', 0, 'Competitor Burned Down', 2, 1.2], #Pen in my Pocket's value is randomized within the game.
    'Electronics Store': ['Theft', 0.8, 'Damaged In Transportation', 0.9, 'Employee Down', 1, 'Local Reviews', 1.1, 'Innovative', 1.2, 'Tech Totalitarian', 2, 1.1],
    'Hardware Store': ['Theft', 0.8, 'Damaged In Transportation', 0.85, 'Work-Related Injury', 1, 'Local Reviews', 1.2, 'As Seen On TV!', 1.1, 'Repair Services', 0, 1.3]
}

#this is all the event text for the game, correlating with the ones above in the list indices (indices, indexes? I don't know)
store_events_messages = {
    'Grocery Store': ['Overnight, there was a problem with the cooling, and some items have gone bad! Lose 20% Cash.', '(This can be prevented with Safer Snacks)', 
                      'Your incoming shipment of goods was lost in transport. Lose 10% Cash.', '(This can be prevented with Transport Training)',
                      'An incident while stocking has left an employee unable to work. Lose 1 employee.', '(Inevitable)',
                      'Locals see your store as the place to shop! Gain 10% Cash.', 'Hooray!',
                      'A new food product has been released that is sweeping the nation, and you got it in your area first! Gain 20% Cash.', 'Way to go!',
                      'Due to competition in the area, a local competitor to your store has shut down. Gain the option to hire 2 employees and 20% Cash.', 'Too easy.'],
    'Convenience Store': ['Petty thieves have taken various items from your store, although they are inexpensive. Lose 2% Cash.', '(This can be prevented with SECURITY)',
                          'Your incoming shipment of goods was lost in transport. Lose 10% Cash.', '(This can be prevented with Transport Training)',
                          'Your store was a victim of attempted robbery and an employee has been shot. Lose 1 Employee.', '(Inevitable)',
                          'Locals see your store as the place to shop! Gain 5% Cash.', 'Hooray!',
                          'A new roadside snack has been released that is sweeping the nation, and you got it in your area first! Gain 10% Cash.', 'Way to go!',
                          'Due to competition in the area, a local competitor to your store has shut down. Gain the option to hire 2 employees and 10% Cash.', 'Too easy.'],
    'Book Store': ['Mild amounts of vandalism have damaged books in your store. Lose 5% Cash.', '(This can be prevented with SECURITY)',
                   'Your incoming shipment of goods was lost in transport. Lose 10% Cash.', '(This can be prevented with Transport Training)',
                   'A shelf has collapsed onto an employee, injuring them. Lose 1 Employee', '(Inevitable)',
                   'Locals see your store as the place to shop! Gain 10% Cash.', 'Hooray!',
                   'You have made a deal with an up and coming author to publish their book in your stores first. Gain either no money or 50% Cash.', 'Read on!',
                   'A local competitor to your store has burned down in a tragic fire. Gain the option to hire 2 employees and 20% Cash.', "It wasn't you, was it?"],
    'Electronics Store': ['Overnight, a theft occured at your store, stealing many important products. Lose 20% Cash.', '(This can be prevented with SECURITY)',
                          'Your incoming shipment of goods has experienced unexpected damage, making them unsellable. Lose 10% Cash.', '(This can be prevented with Transport Training)',
                          'An employee was caught in the middle of a robbery and was injured. Lose 1 Employee', '(Inevitable)',
                          'Locals see your store as the place to shop! Gain 10% Cash.', 'Hooray!',
                          "A new must-have piece of technology is sweeping the nation, and you got it in your area first! Gain 20% Cash.", 'Way to go!',
                          'Local electronic stores in your area have closed, but only you remain. Gain the option to hire 2 employees and 10% Cash.', 'You and you alone.'],
    'Hardware Store': ['Overnight, a theft occured at your store, stealing many important products. Lose 20% Cash.', '(This can be prevented with SECURITY)',
                       'Your incoming shipment of goods has experienced unexpected damage, making them unsellable. Lose 15% Cash.', '(This can be prevented with Transport Training)',
                       'A work-related accident has put one of your employees out of work. Lose 1 Employee.', '(Inevitable)',
                       'Locals see your store as the place to shop! Gain 20% Cash.', 'Hooray!',
                       'Products that have appeared on TV are now appearing on your shelves. Gain 10% Cash.', 'BILLY MAYS HERE!',
                       'Your shop is contracted to provide repairs for an upper-class area by the city. Gain 30% Cash.', 'Money is great :D']
}

#game stats that will change throughout
store_statistics = {
    'Money': 0,
    'Employees': 0,
    'Products': [],
    'Product Prices': [],
    'Product Quantities': [],
    'Product Original Costs': [],
    'Daily People': 0,
    'Product Costs': []
}
clear()

#initial stuff
print("Welcome to Store Manager!\n\nThis game will let you manage your own store.\n")
print("You will have 30 days to build a store and pass an inspection.\nAfter that, the game can be played infinitely! \n")

print("Select a store type from the list below: \n")

#this prints all the store types
for i in range(1, len(store_types)+1):
    i = str(i)
    print(f"{i}: {store_types[i]}")

#spacing
print()

#this solution is bad, but it works
#if the store selection isnt valid, it loops until it is (store_selection assigned beforehand)
while (type(store_selection) != int) or store_selection < 1 or store_selection > 5:
    store_selection = input("Enter the number of the store you want to select [1-5]: ")
    store_selection = tryToConvert(store_selection)
    if (type(store_selection) != int) or store_selection < 1 or store_selection > 5:
        continue

#Makes store_selection a string and assigns it to the name of the store chosen
store_selection = str(store_selection)
store_selection = store_types[store_selection]

print(f"\nStore Selected: {store_selection}.\n")
print("Next you'll need to decide your store name.")
#loop if someone wants to change the store name, store_name variable is assigned beforehand, so there isn't
#two input statements. An invalid input (not y or n) will just cause the program to continue
while store_name == '':
    store_name = input("Enter your store's name: ")
    print(f"\nYou chose {store_name} as your store's name.\n")

    keep_name = input("Would you like to keep this name?[y/n]: ").lower()
    if keep_name == 'n':
        store_name = ''
    if keep_name != 'y' and keep_name != 'n':
        print("Invalid input. Continuing...")

#assigns the starting values of the specified store to the game values
store_statistics['Money'] = store_starting_stuff[store_selection][0]
store_statistics['Employees'] = store_starting_stuff[store_selection][1]
store_statistics['Daily People'] = store_starting_stuff[store_selection][2]

#spacing
print()

#main game loop
while Game == True:

    #allows another employee to be hired
    hire_employee = True

    #clear screen each day
    clear()

    #variable for multiple loops
    day = True
    
    #counts the amount of days, will announce inspection day
    day_count += 1
    print(f"Day {day_count}.")
    if day_count == 30:
        keep_playing = ''
        first_loss = False
        second_loss = False
        print("INSPECTION DAY")
        print("\n\n")
        sleep(5)
        print("Today, your store will be inspected to see if it has reached acceptable circumstances.\n")
        sleep(2)
        print("First we will inspect your cleanliness...")
        sleep(1)
        print("...")

        #checks if the cleanliness rating is high enough
        if alphabet_list.index(cleanliness_rating) > 1:
            print("\nI'm sorry, but your store does not reach mandated cleanliness. You will have to shut down.")
            Game = False
            continue
        else:
            print("\nGood. Your store seems to be clean.")

        print("We have passed around a survey about how stressed your employees feel. We will read the results now...")
        sleep(1)
        print("...")

        #checks if stress has reached 8 or higher
        if stress >= 8:
            print(f"\nWith a stress level of {stress}, your employees seem to be overworked. You will lose points for this.")
            first_loss = True
        else:
            print(f"\nWith a stress level of {stress}, your employees seem quite happy here. Good work.")
        
        print("Finally, we would like to see if you are turning a profit with this business.\n")
        sleep(2)
        print("Please hand over your financial paperwork.\n")
        sleep(1)
        print("...")

        #checks if starting money is less than current money
        if store_statistics['Money'] > store_starting_stuff[store_selection][0]:
            print("\nYou seem to be doing pretty well here. Good work.")
        else:
            print("\nYou don't seem to be doing to well on financials. We will take points off for this.")
            second_loss = True
        
        sleep(4)
        if first_loss == True and second_loss == True:
            print("\nThe way you run this store is utterly unacceptable. You have failed this inspection and will have to shut down.")
            Game = False
            continue
        elif first_loss == True and second_loss == False:
            print("\nYou run this place... well enough. Profits are in the green, but your employees are stressed. Fix that. Otherwise, you pass.")
            print("\n\n\n\n\n\t\tVICTORY")
        elif first_loss == False and second_loss == True:
            print("\nYou run this place... well enough. You seem to be focusing on your employees, which is good, but so is staying in the green. Otherwise, you pass.")
            print("\n\n\n\n\n\t\tVICTORY")
        elif first_loss == False and second_loss == False:
            print("\nI must say, you run an immaculate store. I wish you well with all future endeavors. You pass, with flying colors.")
            print("\n\n\n\n\n\t\tVICTORY")
        while keep_playing != 'y' and keep_playing != 'n':
            keep_playing = input("Would you like to keep playing? [y/n]: ")
            if keep_playing != 'y' and keep_playing != 'n':
                invalid_message()
                continue
        if keep_playing == 'n':
            Game = False
        continue

        
    
    if day_count > 7:
        random_stress = random.randint(1,6)
        if random_stress == 1:
            stress += 1

    #see NOTES, under EVENTS
    if day_count == 6:
        print("IMPORTANT: Every 5th day from now on, there will be a random event that will either benefit or negatively affect your store.")
        enter_to_continue = input("Press Enter to Continue")
    if day_count > 5:
        dirty_store = random.randint(1,10)
        if dirty_store == '1':
            cleanliness_rating = alphabet_list[cleanliness_rating+1]
            print("Your store is getting dirty. You might want to fix that.\n")
            print("Hint: Look under 'Manage Employees'.")
            if alphabet_list.index(cleanliness_rating) >= 2:
                print("WARNING: YOU ARE AT RISK FOR NOT PASSING INSPECTION.")
        checkForEvent()
    
    #temp_stress used for loop
    temp_stress = stress

    #start the stress meter string
    stress_meter = "["

    #add a bar for each stress 
    while temp_stress > 0:
        stress_meter = str(stress_meter) + "|"
        temp_stress -= 1

    #if the stress meter isn't full, add dots to represent blank slots
    if stress_meter.count('|') != 16:
        #loop using gap measure, which is the remainder of spaces needed after the bars
        gap_measure = 16 - stress
        while gap_measure > 0:
            stress_meter = stress_meter + "."
            gap_measure -= 1

    #close stress meter
    stress_meter = stress_meter + ']'

    #print it
    print("\n\nSTRESS:")
    print(stress_meter)

    if stress != 0:
        #weird version of the exponential growth equation
        #used to check if an employee will quit
        quit_math = round(stress*(1+.03)**stress)
        quit_random = random.randint(1,100)
        #See NOTES, I can't explain it well here
        if quit_random < quit_math:
            store_statistics['Employees'] -= 1
            print("One of your employees have left due to stress! \n")
            stress += 1
            print("+1 Stress")

    #tutorial
    if day_count == 1:
        print("\nWelcome to your store!\n")
        print("Your job is to grow your store and keep it well put together to pass inspection day.\n\n")
        print("Every day, you can pick an option from the list below\n")
        sleep(0)
        options_list()
        tutorial_choose = input("\nType 1 to buy more products: ")

        while tutorial_choose != '1':
            invalid_message()
            tutorial_choose = input("\nType 1 to buy more products: ")

        print("\nWhen it comes to purchasing items, you can decide to purchase\nwhatever products you want, and set any price for those items.")
        sleep(0)
        print("\nCustomers will decide if they want to buy that item based off the price.\nThere is some randomness, of course, but this is the general principle of solving it.\n\n")
        sleep(0)
        print("You need to have at least 3 items in your store before starting.\n")
        print("Once you finish entering the items you want to buy, simply type END.\n")
        sleep(0)
        addProduct()
        print("\nYou can add a product to the list of items you want to sell anytime you want.\nYou can also remove items from the list as well.")

    customerGenerator()

    print(f"Money: ${store_statistics['Money']:.2f}")
    print(f"Employees: {store_statistics['Employees']}\n")
    print(f"Cleanliness Rating: {cleanliness_rating}")

    #prints all the products, prices, and quantities
    if len(store_statistics['Products']) > 0:
        print("Products:\t\tPrice:\t\tQuantity:")
        for x in range(len(store_statistics['Products'])):
            print(f"{store_statistics['Products'][x]}\t\t\t${store_statistics['Product Prices'][x]:.2f}\t\t{store_statistics['Product Quantities'][x]}")

    while day == True:

        #spacing
        print()

        choose_option = ''
        options_list()

        #spacing
        print()

        while (type(choose_option) != int) or choose_option < 1 or choose_option > 6:
            choose_option = input("Enter the number you want to use [1-6]: ")
            choose_option = tryToConvert(choose_option)
            continue
        
        #spacing
        print()

        #each option and their corresponding number
        if choose_option == 1:
            addProduct()

        if choose_option == 2:
            hireEmployees()

        if choose_option == 3:
            storeUpgrades()

        if choose_option == 4:
            manageEmployees()

        if choose_option == 5:
            checkInventory()
            
        if choose_option == 6:
            day = False
            continue

        if choose_option < 1 or choose_option > 7:
            invalid_message()
            continue

#Game over
print("GAME OVER")