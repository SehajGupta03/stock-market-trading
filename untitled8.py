###########################################
#
# Computer Project 9
#
# Algorithm
#
# this project accepts the file name for 2 different csv files
# the second file is opened only after the first file is opened successfully
# the security file is read and used to return a set and a dictionary
# the set consists of all companies names
# add_prices function is used to add the information about prices of each company to the values of the keys in the dictionary
# the information about prices is extracted from the prices file
# get_max_price function's purpose is to return the maximum price of the stock of a company and also the time when the price hit maximum
# find_max_company_price function's purpose is to return the company's names and its maximum price
# get_avg_price_of_company function's purpose is to return the company's average price
# in the main funciton, the user is shown a menu. According to which they are used to enter a choice
# Now as per the choice made the functin is made to perfom functions and thus displaying results
# printing output
# closing statements
#
#
#################################################

import csv
import math

MENU = '''\nSelect an option from below:
            (1) Display all companies in the New York Stock Exchange
            (2) Display companies' symbols
            (3) Find max price of a company
            (4) Find the company with the maximum stock price
            (5) Find the average price of a company's stock
            (6) quit
    '''
WELCOME = "Welcome to the New York Stock Exchange.\n"
    
def open_file():
    
    '''This function is used to open 2 files. The second file is not openend till the first file is openend\
    successfullly. It returns two file pointers for both files respectively.'''

    while True:
        try:
            filename=input("\nEnter the price's filename: ")
            fp_price=open(filename,'r')
            break
        except FileNotFoundError:
            print("\nFile not found. Please try again.")
            continue
    while True:
        try:
            filenames=input("\nEnter the security's filename: ")
            fp_securities=open(filenames,'r')
            break
        except FileNotFoundError:
            print("\nFile not found. Please try again.")
            continue
    return fp_price,fp_securities

    

def read_file(securities_fp):
    
    '''This funciton uses the securitites file pointer to read the file and thus creating\
    a master dictionary wherein the keys are the company's symbol and the value is a list of information\
    about the same company. It also returns a set which consists of all the company names.'''

    reader=csv.reader(securities_fp)
    next(reader,None)
    set_row=set()
    dict_master={}
    for row in reader:
        set_row.add(row[1])
        dict_master[row[0]]=[row[1],row[3],row[4],row[5],row[6],[]]
    return set_row,dict_master

        
def add_prices (master_dictionary, prices_file_pointer):
    
    '''This function uses the dictionary created in the read_file function and adds the price related data to the\
    appropriate company. The information related to price about each company is extracted from the price file.'''

    reader=csv.reader(prices_file_pointer)
    next(reader,None)
    for row in reader:
        if row[1] in master_dictionary:
            value=master_dictionary[row[1]]
            l1=[row[0],float(row[2]),float(row[3]),float(row[4]),float(row[5])]
            value[5].append(l1)
    
def get_max_price_of_company (master_dictionary, company_symbol):
    
    '''This function uses the dictonary created in the read_file function to calculate the maximum price of a company. The user enters the\
    symbol of the company they want to know the maximum price of. The function first tests if the provided\
    company symbol is present in the master dictionary or not.'''

    list_tuple=[]
    if company_symbol in master_dictionary:
        value = master_dictionary[company_symbol]
        if value[5]!=[]:
            if len(value[5])>1:
                for i in value[5]:
                    t = (float(i[-1]),str(i[0]))
                    list_tuple.append(t)
            elif len(value[5])==1:
                t = (value[5][0][-1],str(value[5][0][0]))
                list_tuple.append(t)  
        else:
            t=(None,None)
            list_tuple.append(t)
        maximum=max(list_tuple)
        return maximum
    else:
        return (None,None)

def find_max_company_price (master_dictionary):
    
    '''This funciton is used to find the maximum price of the company. It uses the dictionary\
    which is created in the read_file function to perform its task. It returns the list of the company names which has\
    the maximum price.'''

    list_tup=[]
    list_price=[]
    for key in master_dictionary:
        tup=get_max_price_of_company(master_dictionary,key)
        value=master_dictionary[key]
        if value[5]!=[]:
            t=(key,tup[0])
            list_tup.append(t)
            list_price.append(tup[0])
    maximum=max(list_price)
    for i in list_tup:
        if i[1]==maximum:
            return i
    
def get_avg_price_of_company (master_dictionary, company_symbol):
    
    '''This function is used to get the average price of a company whose symbol is provided by the user.'''

    counter=0
    sum_price=0
    if company_symbol not in master_dictionary:
        return 0.0
    else:
        value=master_dictionary[company_symbol]
        if value[5]==[]:
            return 0.0
        else:
            if len(value[5])>1:
                for i in value[5]:
                    counter+=1
                    sum_price+=i[4]
            else:
                sum_price+=value[5][0][4]
                counter=1
    avg=round(sum_price/counter,2)
    return avg

            
def display_list (lst):  # "{:^35s}"
    
    '''This function takes list as a parameter and prints the elements of the list in a tabular form. This\
    function returns nothing.'''

    k=0	
    for i in range(math.ceil(len(lst)/3)):
        for j in range(3):
            print("{:^35s}".format(lst[k]),end="")
            k+=1
            if k==len(lst):
                break
        print()
    if len(lst)%3==0:   
        print("\n")
    else:
        print()
    
def main():
    print(WELCOME)
    
    fp_price,fp_securities=open_file()
    set_row, master_dict = read_file(fp_securities)
    add_prices(master_dict,fp_price)
    
    while True:
        print(MENU)
        choice=int(input("\nOption: "))

        if choice==1:
            print("\n{:^105s}".format("Companies in the New York Stock Market from 2010 to 2016"))
            value=list(master_dict.values())
            value_name=[]
            for i in range(len(value)):
                if value[i][0] not in value_name:
                    value_name.append(value[i][0])
            value_name.sort()
            #print(value_name)
            display_list(value_name)

        elif choice==2:
            print("\ncompanies' symbols:")
            value1=list(master_dict.keys())
            value1.sort()
            display_list(value1)

        elif choice==3:
            while True:
                company_symbol=input("\nEnter company symbol for max price: ")
                if company_symbol not in master_dict:
                    print("\nError: not a company symbol. Please try again.")
                    continue
                else:
                    break
            max_price,date=get_max_price_of_company(master_dict,company_symbol)
            if max_price==None:
                print("\nThere were no prices.")
            else:
                print("\nThe maximum stock price was ${:.2f} on the date {:s}/\n".format(max_price,date))

        elif choice==4:
            max_company, max_price = find_max_company_price(master_dict)
            print("\nThe company with the highest stock price is {:s} with a value of ${:.2f}\n".format(max_company,max_price))
        
        elif choice==5:
            while True:
                company_symbol=input("\nEnter company symbol for average price: ")
                if company_symbol not in master_dict:
                    print("\nError: not a company symbol. Please try again.")
                    continue
                else:
                    break
            avg_price=get_avg_price_of_company(master_dict,company_symbol)
            if avg_price==None:
                print("\nThere were no prices.")
            else:
                print("\nThe average stock price was ${:.2f}.\n".format(avg_price))
        elif choice==6:
            break

        else:
            print("\nInvalid option. Please try again.")
            continue

       
if __name__ == "__main__": 
    main() 


