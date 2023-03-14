def initialize():
    # cur_balance_owing_intst should hold the balance that carries the interest, increasing as necessary,
    # while the cur-balance_owing_recent should hold the purchases made in the latest month without collecting interest.

    global cur_balance_owing_intst, cur_balance_owing_recent

    # Saves the last updated day and month to compare to the newest day and month.
    # Allows the program to collect the right amount of interest.

    global last_update_day, last_update_month

    # Saves the last country and the last-last country to compare and determine whether the card should be deactivated.

    global last_country, last_country2

    # If deactivated is set to True, declines the user from making anymore purchases until the code is reset (initialize()).
    # If deactivated is set to False, allows the program to continue running.

    global deactivated

    cur_balance_owing_intst = 0.0
    cur_balance_owing_recent = 0.0

    last_update_day = 0
    last_update_month = 0

    last_country = None
    last_country2 = None

    deactivated = False

'''Compares the new date to the last recorded date.'''

def date_same_or_later(day1, month1, day2, month2):
    if (month1 == month2 and day1 >= day2) or (month1 > month2):
        return True
    return False

'''Compares the last three countries inputted to check for fraud. Deactivates the credit card if all three are different. Deactivated can then no longer by reactivated / set to False again.'''

def all_three_different(c1, c2, c3):
    global deactivated
    if c1 != c2 and c1 != c3 and c2 != c3 and c2 != None and c3 != None:
        deactivated = True
        return True
    return False

'''Checks if the credit card was deactivated. If not, proceeds to record the owed balances per month.'''

def purchase(amount, day, month, country):
    global cur_balance_owing_intst, cur_balance_owing_recent
    global last_update_day, last_update_month
    global last_country, last_country2
    global deactivated

    '''Checks if the card has been deactivated by comparing the last three countries.'''

    all_three_different(country, last_country, last_country2)
    if date_same_or_later(day, month, last_update_day, last_update_month) == False or deactivated == True:
        return "error"

    if month == last_update_month:
        cur_balance_owing_recent += amount

    # Occurs when the most recent purchase has already started accruing interest that hasn't yet been accounted for.
    # If there is already a balance collecting interest,
    # it collects the updated interest before adding the recent owings (and their interest).
    # Then it collects the required interest for the most recent purchase,
    # moving it to cur_balance_owing_intst and replacing the recent with the newest amount.

    elif month > last_update_month + 1:
        if cur_balance_owing_intst != 0:
            cur_balance_owing_intst *= 1.05**(month - (last_update_month))
        cur_balance_owing_intst += cur_balance_owing_recent * 1.05**(month - (last_update_month + 1))
        cur_balance_owing_recent = amount

    # Occurs when the most recent purchase is not yet collecting balance, but a purchase was made in the next month.
    # If a purchase was made in the month prior, then it moves recent to interest without collecting,
    # and replaces recent with the new purchase amount.
    # However, if there is already a balance in interest, it collects by 1.05 (1 month difference).

    elif month > last_update_month:
        if cur_balance_owing_recent != 0:
            if cur_balance_owing_intst != 0:
                cur_balance_owing_intst *= 1.05
            cur_balance_owing_intst += cur_balance_owing_recent
            cur_balance_owing_recent = amount
        else:
            cur_balance_owing_recent = amount

    updated(day, month)
    last_country, last_country2 = last_country2, last_country
    last_country = country

'''Checks the amount owed at the inputted month. Goes through a list to determine how much interest is applied.'''

def amount_owed(day, month):
    global cur_balance_owing_intst, cur_balance_owing_recent
    global last_update_day, last_update_month
    global last_update_day2, last_update_month2

    if date_same_or_later(day, month, last_update_day, last_update_month) == False:
        return "error"

    # Checks if the current month is past the accruing period for the last-updated month.
    # If there is a balance in recent and a balance in interest, it collects the latter's interest first,
    # before adding the recent on top and recollecting the new total interest.
    # If the new month is only one month after the last updated,
    # then the interest balance is multiplied for a one month difference before adding the recent balance.

    if month > last_update_month + 1:
        if cur_balance_owing_recent != 0:
            if cur_balance_owing_intst != 0:
                cur_balance_owing_intst *= 1.05
            cur_balance_owing_intst += cur_balance_owing_recent
            cur_balance_owing_recent = 0
            cur_balance_owing_intst *= 1.05**(month - (last_update_month + 1))
        else:
            cur_balance_owing_intst *= 1.05**(month - (last_update_month))
    elif month > last_update_month:
        if cur_balance_owing_recent == 0:
            cur_balance_owing_intst *= 1.05
        else:
            cur_balance_owing_intst *= 1.05
            cur_balance_owing_intst += cur_balance_owing_recent
            cur_balance_owing_recent = 0

    updated(day, month)
    return cur_balance_owing_intst + cur_balance_owing_recent

'''Pays bill, prioritizing the balance collecting interest.'''

def pay_bill(amount, day, month):
    global cur_balance_owing_intst, cur_balance_owing_recent
    global last_update_day, last_update_month

    if date_same_or_later(day, month, last_update_day, last_update_month) == False:
        return print("Error")

    # Same program as amount owed.

    if month > last_update_month + 1:
        if cur_balance_owing_recent != 0:
            if cur_balance_owing_intst != 0:
                cur_balance_owing_intst *= 1.05
            cur_balance_owing_intst += cur_balance_owing_recent
            cur_balance_owing_recent = 0
            cur_balance_owing_intst *= 1.05**(month - (last_update_month + 1))
        else:
            cur_balance_owing_intst *= 1.05**(month - (last_update_month))
    elif month > last_update_month:
        if cur_balance_owing_recent == 0:
            cur_balance_owing_intst *= 1.05
        else:
            cur_balance_owing_intst *= 1.05
            cur_balance_owing_intst += cur_balance_owing_recent
            cur_balance_owing_recent = 0

    # Checks if the amount being paid is over the total balance. If it is, returns an error.
    # Otherwise, it removes the amount from the collecting-interest balance,
    # and removes the remaining amount from the recent balance if applicable.

    if amount > (cur_balance_owing_intst + cur_balance_owing_recent):
        return "error"
    elif amount > cur_balance_owing_intst:
        amount -= cur_balance_owing_intst
        cur_balance_owing_intst = 0
        cur_balance_owing_recent -= amount
        amount = 0
    else:
        cur_balance_owing_intst -= amount
        amount = 0
    updated(day, month)

'''Updates the month and day for purchases, amount owed, and bills paid.'''

def updated(day, month):
    global last_update_day, last_update_month

    last_update_day = day
    last_update_month = month

initialize()

## Testing Cases

if __name__ == '__main__':
    # Basic addition with interest and pay off.
    print("Testing Case [1]")
    purchase(10, 1, 1, "Canada") # 10
    purchase(10, 2, 2, "Canada") # 10 + 10 = 20
    purchase(10, 3, 3, "Canada") # 10*1.05 + 10 + 10 = 30.5
    purchase(10, 4, 4, "Canada") # 10*1.05*1.05 + 10*1.05 + 10 + 10 = 41.525
    print("Now owing:", amount_owed(4, 4)) # 41.525
    print("Now owing:", amount_owed(6, 6)) # 45.2563125
    pay_bill(45.2563125, 6, 6) # 45.2563125 - 45.2563125 = 0
    print("Now owing:", amount_owed(6, 6)) # 0

    # Purchases with fraud.
    print("\nTesting Case [2]")
    initialize()
    purchase(10, 1, 1, "Canada") # 10
    purchase(10, 2, 2, "France") # 10 + 10 = 20
    print("Now owing:", amount_owed(2, 2)) # 20
    purchase(10, 3, 3, "China") # Error, card was deactivated due to too many locations.
    print("Now owing:", amount_owed(4, 4)) # 21.525
    purchase(10, 5, 5, "China") # Error, card is still deactivated.

    # Paying off in full before new purchases.
    print("\nTesting Case [3]")
    initialize()
    purchase(50, 1, 1, "Canada") # 50
    print("Now owing:", amount_owed(4, 6)) # 60.7753125
    pay_bill(60.77531250000001, 4, 6)
    print("Now owing:", amount_owed(4, 7)) # 0
    purchase(50, 1, 8, "Canada")
    print("Now owing:", amount_owed(25, 12)) # 57.88125

    # Paying off partially before new purchases.
    print("\nTesting Case [4]")
    initialize()
    purchase(50, 1, 1, "Canada") # 50
    print("Now owing:", amount_owed(4, 6)) # 60.7753125
    pay_bill(30, 4, 6)
    print("Now owing:", amount_owed(4, 6)) # 30.7753125
    print("Now owing:", amount_owed(4, 8)) # 30.7753125*1.05*1.05 = 33.92978203
    purchase(50, 1, 10, "Canada") # 33.929782031250014*1.05*1.05 + 50
    print("Now owing:", amount_owed(1, 10)) # 87.4075846895
    print("Now owing:", amount_owed(25, 12)) # 93.7418621201

    # Paying off twice, not in full.
    print("\nTesting Case [5]")
    initialize()
    purchase(50, 1, 1, "Canada") # 50
    print("Now owing:", amount_owed(1, 3)) # 52.5
    pay_bill(27.5, 3, 3) # 52.5 - 27.5 = 25
    print("Now owing:", amount_owed(1, 5)) # 25*1.05*1.05 = 27.5625
    pay_bill(17.5625, 5, 5) # 27.5625 - 17.5625 = 10
    print("Now owing:", amount_owed(1, 12)) # 10*1.05^7 = 14.07100432

    # Paying off twice, not in full and with new purchases.
    print("\nTesting Case [6]")
    initialize()
    purchase(50, 1, 1, "Canada") # 50
    print("Now owing:", amount_owed(1, 3)) # 52.5
    pay_bill(27.5, 3, 3) # 52.5 - 27.5 = 25
    purchase(50, 3, 3, "France")
    print("Now owing:", amount_owed(1, 5)) # 25*1.05*1.05 + 50*1.05 = 80.0625
    pay_bill(17.5625, 5, 5) # 80.0625 - 17.5625 = 62.5
    print("Now owing:", amount_owed(1, 12)) # 62.5*1.05^7 = 87.94377642

    # Paying off twice, not in full and with new purchases / three different countries
    print("\nTesting Case [7]")
    initialize()
    purchase(50, 1, 1, "Canada") # 50
    print("Now owing:", amount_owed(1, 3)) # 52.5
    pay_bill(27.5, 3, 3) # 52.5 - 27.5 = 25
    purchase(50, 3, 3, "France")
    print("Now owing:", amount_owed(1, 5)) # 25*1.05*1.05 + 50*1.05 = 80.0625
    pay_bill(17.5625, 5, 5) # 80.0625 - 17.5625 = 62.5
    purchase(50, 1, 6, "China") # Error, card deactivated due to three different countries.
    purchase(50, 1, 6, "Canada") # Error, card is still deactivated.
    print("Now owing:", amount_owed(1, 12)) # 62.5*1.05^7 = 87.94377642

    # Purchasing twice in a row before paying off partially.
    print("\nTesting Case [8]")
    initialize()
    purchase(100, 1, 1, "Canada") # 100
    purchase(40, 1, 2, "France") # 100 + 40 = 140
    print("Now owing:", amount_owed(1 ,2)) # 140
    purchase(40, 1, 2, "China") # Error, card deactivated due to three different countries.
    print("Now owing:", amount_owed(1 ,2)) # 140
    print("Now owing:", amount_owed(1 ,3)) # 100*1.05 + 40 = 145
    print("Now owing:", amount_owed(31 ,3)) # 145
    print("Now owing:", amount_owed(1 ,4)) # 100*1.05*1.05 + 40*1.05 = 152.25
    print("Now owing:", amount_owed(1 ,8))
    pay_bill(75, 1, 8) # (100*1.05^6 + 40*1.05^5) - 75 = 185.0608266 - 75 = 110.0608266
    print("Now owing:", amount_owed(1 ,8))

    # Purchases over large time spans with alternating locations.
    print("\nTesting Case [9]")
    initialize()
    purchase(50, 1, 1, "Canada") # 50
    purchase(50, 6, 6, "France") # 50*1.05^4 + 50
    print("Now owing:", amount_owed(6, 6)) # 110.7753125
    purchase(50, 12, 12, "Canada")
    print("Now owing:", amount_owed(12, 12)) # 50*1.05^10 + 50*1.05^5 + 50 = 195.258809464