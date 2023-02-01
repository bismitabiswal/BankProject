# Importing Pandas to create DataFrame
import pandas as pd
from random import randint
from datetime import datetime


def ActionRequired(present_df):
    try:
        print("Choose your Action")
        df = pd.DataFrame()
        while True:
            action = int(input("Enter 1 for 'Create Account' \n Enter 2 for 'Account Deposit' \n Enter 3 for 'Account Withdrawal' \n Enter 4 for 'Account Transfer' \n Enter 5 for 'Quit'"))
            if action ==1:
                print("Create Account")
                newdf= InputCustomerInfo(present_df)
                newdf.to_csv(r'C:\Users\bismi\Desktop\PythonProjects\BankProject\OutputData\output.csv',index=False)
                return newdf
            elif action ==2:
                print("Account Deposit")
                df = df.append(deposit(present_df), ignore_index=True)
                path_nm = r'C:\Users\bismi\Desktop\PythonProjects\BankProject\OutputData\Deposit.xlsx'
                write_into_excel(df,path_nm)
                return df
            elif action ==3:
                print("Account Withdrawal")
                df = df.append(withdraw(present_df), ignore_index=True)
                path_nm = r'C:\Users\bismi\Desktop\PythonProjects\BankProject\OutputData\Withdraw.xlsx'
                write_into_excel(df,path_nm)
                return df
            elif action ==4:
                print("Account Transfer")
                df = df.append(transfer(present_df), ignore_index=True)
                path_nm = r'C:\Users\bismi\Desktop\PythonProjects\BankProject\OutputData\Transfer.xlsx'
                write_into_excel(df,path_nm)
                return df
            elif action ==5:
                outcome = input("Are you sure you want to quit : yes/no")
                quit(outcome)
                break
    except Exception as error:
        print('Caught this error in ActionRequired function : ' + repr(error))

def write_into_excel(df,path_nm):
    try:
        old_df = pd.read_excel(path_nm)
        if old_df.empty :
            df.to_excel(path_nm ,index=False )
        else :
            new_df = old_df.append(df, ignore_index=True)
            new_df.to_excel(path_nm ,index=False )
    except Exception as error:
        print('Caught this error in write_into_excel function : ' + repr(error))
            
def AccountNumberCheck(a,df):
    try:
        print("Checking the Created New AccountNumber, if it already exists")
        if a in df.values :
            b =''.join(["{}".format(randint(0, 9)) for num in range(0, 10)])
            if b != a :
                return b
        else :
            return a
    except Exception as error:
        print('Caught this error in AccountNumberCheck function : ' + repr(error))

def InputCustomerInfo(present_df):
    try:
        dictionary={}
        df1 = pd.DataFrame()
        print("Starting to take customer Information")
        name = input("Enter your name: ")
        dictionary["name"] = name

        Address = input("Enter your Address: ")
        dictionary["Address"] = Address

        Pincode = input("Enter your Pincode: ")
        dictionary["Pincode"] = Pincode

        IdentityProof = input("Enter your IdentityProof: ")
        dictionary["IdentityProof"] = IdentityProof

        Phoneno = int(input("Enter your Phoneno: "))
        dictionary["Phoneno"] = Phoneno
        if len(str(Phoneno)) != 10 :
            outcome = "Invalid phone number entered , Please restart the process"
            Phoneno = int(input("Enter your Phoneno: "))
            dictionary["Phoneno"] = Phoneno

        Account = int(input("Account Type 1 for Savings Account and 2 for Checking Account: "))
        if Account == 1:
            AccountType = 'Savings'
        elif Account == 2:
            AccountType = 'Checking'
        dictionary["AccountType"] = AccountType

        a=''.join(["{}".format(randint(0, 9)) for num in range(0, 10)])
        if present_df.empty:
            print("No Check Move ahead")
            dictionary["AccountNumber"] = a
        else:
            a = AccountNumberCheck(a,present_df)
            dictionary["AccountNumber"] = a

        print("Your Account is created. \n Account Number :", a)

        amount = int(input("Enter your Amount: "))
        dictionary["Amount"] = amount

        df1= df1.append(dictionary, ignore_index=True)
        df_merged = df1.append(present_df, ignore_index=True)
        print("df1")
        print(df1.head())
        print("df1")
        print(df_merged.head())
        return df_merged
    except Exception as error:
        print('Caught this error in InputCustomerInfo function : ' + repr(error))

def account_number_input(present_df):
    try:
        account_number = int(input("Enter the Account Number :"))
        if account_number in present_df['AccountNumber'].unique():
            df = present_df.loc[(present_df['AccountNumber'] == account_number)]
            # below commented ones can be commented incase of easy input of data
            #print(df)
            #print(df['name'].values[0])
            #print(df['Phoneno'].values[0])
            check_customer(df)
            get_balance(df)
            return df
        else :
            print("Invalid account Number entered")
            ActionRequired(present_df)
    except Exception as error:
        print('Caught this error in account_number_input function : ' + repr(error))
        
def check_customer(df):
    try:
        print("Please enter the below details to help us validate the account")
        customer_name = input("Enter the Cutomer Name: ")
        phone_number = int(input("Enter the Customer's Phone Number: "))
        if df['name'].values[0] == customer_name and df['Phoneno'].values[0] == phone_number:
            print("Account is Validated")
        else :
            print("This account doesnot belong to the customer entered \n Aborting the process")
            outcome = "This account doesnot belong to the customer entered \n Aborting the process"
            quit(outcome)
    except Exception as error:
        print('Caught this error in check_customer function : ' + repr(error))

def get_balance(df):
    try:
        amount = df['Amount'].values[0]
        print("Present account balance is: ", amount)
    except Exception as error:
        print('Caught this error in get_balance function : ' + repr(error))

def deposit(present_df):
    try:
        df = account_number_input(present_df)
        new_deposit = {}
        deposit_amount = int(input("Enter the amount to be deposited :"))
        new_deposit["Previous Amount"] = df['Amount'].values[0]
        new_deposit["Amount Deposited"] = deposit_amount
        if deposit_amount >= 0 :
            print("Processing Deposit")
            amount = df['Amount'].values[0] + deposit_amount
            depositor = int(input("1 for Self Depositor 2 for Entering name"))
            if depositor == 1 :
                depositor_name = df['name'].values[0]
                print("Self Deposit: ", depositor_name)
                new_deposit["Deposited By"] = "Self Deposit:" + depositor_name
            elif depositor == 2:
                depositor_name = input("Deposited by :")
                print("Deposited by :" , depositor_name)
                new_deposit["Deposited By"] = depositor_name
            new_deposit["Present Amount"] = amount
            new_deposit["Deposit DateTime"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            update_amount(df ,present_df , amount)
            return new_deposit
        else :
            print("Invalid amount entered")
            ask = input("Do you want to re-enter the amount and continue with the deposit : yes/no")
            if ask == "yes":
                print("Please enter valid amount")
                new_deposit=deposit(present_df)
                return new_deposit
            else :
                outcome = "Deposit process ended"
                quit(outcome)
    except Exception as error:
        print('Caught this error in deposit function : ' + repr(error))

def withdraw(present_df):
    try:
        df = account_number_input(present_df)
        new_withdraw = {}
        withdrawal_amount = int(input("Enter the amount to be withdraw :"))
        new_withdraw["Previous Amount"] = df['Amount'].values[0]
        new_withdraw["Amount Withdraw"] = withdrawal_amount
        if withdrawal_amount <= df['Amount'].values[0] and withdrawal_amount >=0 :
            print("Processing Withdraw")
            amount = df['Amount'].values[0] - withdrawal_amount
            new_withdraw["Present Amount"] = amount
            new_withdraw["Withdrawal DateTime"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            update_amount(df ,present_df , amount)
            return new_withdraw
        elif withdrawal_amount > df['Amount'].values[0] :
            print("Insufficient Balance")
            ask = input("Do you want to re-enter the withdrawal amount")
            if ask == "yes":
                new_withdraw=withdraw(present_df)
                return new_withdraw
            else :
                outcome = "Withdrawal process ended"
                quit(outcome)
        elif withdrawal_amount <=0 :
            print("Invalid amount entered")
            ask = input("Do you want to re-enter the withdrawal amount")
            if ask == "yes":
                new_withdraw=withdraw(present_df)
                return new_withdraw
            else :
                outcome = "Withdrawal process ended"
                quit(outcome)
    except Exception as error:
        print('Caught this error in withdraw function : ' + repr(error))

def transfer(present_df):
    try:
        print("Sender's account")
        sender_df = account_number_input(present_df)
        print("Receiver's account")
        receiver_df = account_number_input(present_df)
        new_transfer = {}
        new_transfer["Sender's account"] = sender_df['AccountNumber'].values[0]
        new_transfer["Receiver's account"] = receiver_df['AccountNumber'].values[0]
        transfer_amount = int(input("Enter the amount you want to transfer :"))
        if transfer_amount <= sender_df['Amount'].values[0] and transfer_amount >=0 :
            print("Processing Transfer")
            sender_amount = sender_df['Amount'].values[0] - transfer_amount
            receiver_amount = receiver_df['Amount'].values[0] + transfer_amount
            new_transfer["Sender's Present Amount"] = sender_amount
            update_amount(sender_df ,present_df , sender_amount)
            new_transfer["Transfer Amount"] = transfer_amount
            new_transfer["Receiver's Present Amount"] = receiver_amount
            update_amount(receiver_df ,present_df , receiver_amount)
            new_transfer["Transfer DateTime"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            return new_transfer
        elif transfer_amount > sender_df['Amount'].values[0] :
            print("Insufficient Balance")
            ask = input("Do you want to redo the transfer : yes/no")
            if ask == "yes":
                new_transfer = transfer(present_df)
                return new_transfer
            else :
                outcome = "Transfer process ended"
                quit(outcome)
        elif transfer_amount <=0 :
            print("Invalid amount entered")
            ask = input("Do you want to redo the transfer : yes/no")
            if ask == "yes":
                new_transfer = transfer(present_df)
                return new_transfer
            else :
                outcome = "Transfer process ended"
                quit(outcome)
    except Exception as error:
        print('Caught this error in transfer function : ' + repr(error))

def update_amount(df ,present_df , new_amount):
    try:
        account_number = df['AccountNumber'].values[0]
        cond = (present_df['AccountNumber'] == account_number)
        present_df.loc[cond,'Amount'] = new_amount
        present_df.to_csv(r'C:\Users\bismi\Desktop\PythonProjects\BankProject\OutputData\output.csv',index=False)
    except Exception as error:
        print('Caught this error in update_amount function : ' + repr(error))

def quit(outcome):
    try:
        if outcome == "yes" :
            print("No action performed")
        else :
            print(outcome)
            again = input("Do you want to retry")
            if again == "yes" :
                main(again)
            else :
                outcome = 'yes'
                quit(outcome)
    except Exception as error:
        print('Caught this error in quit function : ' + repr(error))

def main(help):
    try:
        present_df = pd.read_csv(r'C:\Users\bismi\Desktop\PythonProjects\BankProject\OutputData\output.csv')
        while True:
            #help = input("Enter Yes/No :")
            if help == 'yes' :
                df =ActionRequired(present_df)
                print(df)
                return df
            else :
                break
    except Exception as error:
        print('Caught this error in main function : ' + repr(error))
if __name__ == "__main__":
    while True:
        x = input("Do you want to perform any Operation : yes /no ")
        if x == 'yes' :
            main(x)
        else :
            print("Thank you for the Patience")
            break