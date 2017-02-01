"""
Introduction to Web Science
Assignment 10
exercise 2
Team : golf

"""
import random
import matplotlib.pyplot as plt

# function to sum nested lists
def sum_nested(l):
    s = 0
    for item in l:
        if type(item) is list:
            s += sum_nested(item)
        else:
            s += item
    return s
# function to calculate the gini given a list of shares
def calculateGini(shares,n):
    return 1/(2*n)*(sum_nested(abs(shares[i] - shares[j]) for j in range(0,n) 
                    for i in range(0,n))/sum(shares[i] for i in range(0,n))) 
    
def generateChineseRestaurant(customers):
    # First customer always sits at the first table
    tables = [1]
    ginis=[0]
    #for all other customers do
    for cust in range(2, customers+1):
            # rand between 0 and 1
            rand = random.random()
            # Total probability to sit at a table
            prob = 0
            # No table found yet
            table_found = False
            # Iterate over tables
            for table, guests in enumerate(tables):
                # calc probability for actual table an add it to total 
                # probability
                prob += guests / (cust)
                # If rand is smaller than the current total prob., 
                # customer will sit down at current table
                if rand < prob:
                    # incr. #customers for that table
                    tables[table] += 1
                    # customer has found table
                    table_found = True
                    # no more tables need to be iterated, break out for loop
                    break
            # If table iteration is over and no table was found, open new table
            if not table_found:
                tables.append(1)
            # we calculate the share of every table 
            table_shares=[g/cust for g in tables]
            # then we calculate the gini for the current number of customers
            ginis.append(calculateGini(table_shares,len(tables)))
    return tables,ginis
    

    
restaurants = 1000
for i in range(0,5):
    network,gcoefs = generateChineseRestaurant(restaurants)
    plt.plot(range(1,restaurants+1), gcoefs, 'b')
plt.xlabel("Customers")
plt.ylabel("Gini")
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.show()


