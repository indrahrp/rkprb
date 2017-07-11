from pprint import pprint
import getopt, sys
import MySQLdb
from datetime import datetime,date,timedelta
#from mysql.connector import MySQLConnection, Error

query_all_list=[]
db = MySQLdb.connect("localhost","root","Nabraf10","accountinfo" )
#dbtask=MySQLdb.connect("localhost","root","Nabraf10","accountinfo" )
def column_list(table):
	columnlist=[]
	cursor=db.cursor()
	sql = "Select * from " + table
	#print "sql " + sql
	cursor.execute(sql)
	desc = cursor.description
	for row in desc:
		#print "desc isi "+ row[0]
		columnlist.append(row[0])
	return columnlist


class Account (object):
	def __init__(self,account_name,owner='coki',account_type='Credit',duedate='none',apr='none',balance='0',logname='',pwd=''):
		self.account_name=account_name
		self.account_type=account_type
		self.owner=owner
		self.duedate=duedate
		self.apr=apr
		self.balance=balance
		self.logname=logname
		self.pwd=pwd
		self.listinfo=[account_name,account_type,duedate,apr,balance,logname,pwd]
		
	def check_fivedays_beforedue (self):
		print("due date " + self.duedate)
	
	def printattr(self):
		pprint(self.listinfo)
		

def Insert_AccountTable(account_name,account_type,owner,duedate,apr,balance,logname,pwd):
	
	# prepare a cursor object using cursor() method
	cursor = db.cursor()
	
	sql = "Insert into account(account_name,account_type,owner,duedate,apr,balance,logname,pwd) values (%s,%s,%s,%s,%s,%s,%s,%s)"
	args = (account_name,account_type,owner,duedate,apr,balance,logname,pwd)
	#print ('in insert account table function')
	try:
		# Execute the SQL command
		print "insert execute completed"
		cursor.execute(sql,args)
		result = cursor.fetchall()
		print result
		print "insert execute completed"
		# Commit your changes in the database
		db.commit()	
		# Rollback in case there is any error
	except MySQLdb.Error as e:
		#if e[0]!= ###:
		raise
		db.rollback()

		# disconnect from server
	db.close()
	
def Query_AccountTable(account_name):
	# prepare a cursor object using cursor() method
	global query_all_list
	cursor = db.cursor()
	if account_name=='all':
		sql = "Select * from account "
	else:
		sql = "Select * from account where account_name=%s "
		args = account_name
	#print ('in select account table function for accountname '+args)
	try:
	
		# Execute the SQL command
		#print "select execute completed"
		if account_name=='all':
			noofrows=cursor.execute(sql)
			#print(noofrows)
		else:
			print "in query "
			noofrows=cursor.execute(sql,[args])
			#print(noofrows)
		
		desc = cursor.description
		#print "%-2s %-17s %-10s %-10s %-20s %-10s %-10s" % (desc[0][0].strip(), desc[1][0].strip(), desc[2][0].strip(), desc[3][0].strip(), desc[4][0], desc[5][0], desc[6][0])
		#print (desc[0][0].center(2) +  desc[1][0].center(20) + desc[2][0].center(20) + desc[3][0].center(10) +  desc[4][0].center(20) + desc[5][0].center(10)+ str(desc[6][0]).center(10))
		print (desc[0][0].rjust(2) +  desc[1][0].rjust(20) + desc[2][0].rjust(20) + desc[3][0].rjust(16) +  desc[4][0].rjust(8) + desc[5][0].rjust(15)+ str(desc[6][0]).rjust(10) + desc[7][0].rjust(20) + desc[8][0].rjust(15))
		print "\n==============================================================================================================================================================\n"
		for row in cursor.fetchall():
			id=row[0]
			account_name=row[1]
			account_type = row[2]
			owner = row[3]
			duedate = row[4]
			apr = row[5]
			balance = row[6]
			logname = row[7]
			pwd = row[8]
			#print (str(id).center(2) +  account_name.center(20) + account_type.center(20) + owner.center(10) +  duedate.center(20) + apr.center(10) + str(balance).center(5))
			print (str(id).rjust(2) +  account_name.rjust(20) + account_type.rjust(20) + owner.rjust(16) +  duedate.rjust(8) + apr.rjust(15) + str(balance).rjust(10)+ logname.rjust(20)+ pwd.rjust(15))
			query_all_list.append(row)
	except MySQLdb.Error as e:
		print(e)
			
	#db.close()
	#print('Account_Name :' + account_name + '\nOwner \nduedate : ' + duedate + '\nAPR :' + apr + '\nBalance :' + str(balance))
	

def Delete_AccountTable(account_name):

	cursor = db.cursor()
	sql = "Delete from account where account_name=%s"
	args = (account_name)
	print ('in delete account table function')
	try:
		# Execute the SQL command
		print " in delete execute "
		cursor.execute(sql,[args])
		result = cursor.fetchall()
		print result
		print "delet execute completed"
		# Commit your changes in the database
		db.commit()	
		# Rollback in case there is any error
	except MySQLdb.Error as e:
		#if e[0]!= ###:
		raise
		db.rollback()
	db.close()
		

		
def Update_Account(account_name,columntoupdate,newvalue):
	
	cursor = db.cursor()
	
	sql = "update account set " + columntoupdate + "=%s where account_name= %s"
	args = [newvalue,account_name]
	#print sql
	#print (' update account table function')
	try:
		#print " in update execute "
		cursor.execute(sql,args)
		result = cursor.fetchall()
		#print result
		#print "update execute completed"
		db.commit()	
	except MySQLdb.Error as e:
		raise
		db.rollback()
	db.close()

def get_whattoupdate(account_name):
	
	Query_AccountTable(account_name)
	columnlist=column_list('account')
	columntoupdate=raw_input('\n\nenter what column to update: ')
	
	if columntoupdate not in 'qQ':
		if columntoupdate not in columnlist:
			print " incorrect column name"
			exit(0)
		else:
			newvalue=raw_input('\n\nwhat is new column value (q or Q to exit) of ' + columntoupdate + ' : ')
			if newvalue not in 'qQ':
				Update_Account(account_name,columntoupdate,newvalue)
	else:
		exit(0)
	
def enter_account_info():
	answer='no'
	while answer != 'ok':
	
		account_name=raw_input('\n\nenter account_name (q or Q to exit): ')
		if account_name in 'qQ':
			exit(0)
		else:	
			owner=raw_input('enter owner : ')
			account_type=raw_input('enter account_type : ')
			duedate=raw_input('enter payment due date : ')
			apr=raw_input('enter APR : ')
			balance=raw_input('enter balance : ')
			logname=raw_input('enter login name: ')
			pwd=raw_input('enter passwd : ')
			
			answer=raw_input('Enter ok if data is ok  :')
		
	account=Account(account_name,owner,account_type,duedate,apr,balance,logname,pwd)
	print ("you entered" + account_name + owner + duedate + apr + balance + logname + pwd )
	Insert_AccountTable(account.account_name,account.account_type,account.owner,account.duedate,account.apr,account.balance,logname,pwd)
	return account

def query_account_info():
	account_name=raw_input('enter account_name to retrieve the information or type all for ALL account info :')
	Query_AccountTable(account_name)
	

def Delete_Account(account_name):
	Delete_AccountTable(account_name)
	
def getaccount_due_soon():
	daysdueneed=7
	td=timedelta()
	now=date.today()
	#now=date(2016,12,12)
	current_month=now.month
	#print 'now ' + now.strftime("%m/%d/%y") + ' ' + str(current_month)
		
	del query_all_list[:]
	Query_AccountTable('all')
	for idx in query_all_list:
		if idx[4]=='na':
			print "account "+ idx[1] + " does not have duedate"
		else:
			duefromaccount=int(idx[4])
			#print "duefaomaccount " + str (duefromaccount)
			if duefromaccount >= now.day:
				duedate=date(now.year,now.month,duefromaccount)
			elif duefromaccount < now.day and now.month==12:
				duedate=date(now.year+1,1,duefromaccount)
			else:
				duedate=date(now.year,now.month+1,duefromaccount)
			#	print 'duedate ' + duedate.strftime("%m/%d/%y")
			td = duedate - now
			#print "td " + str(td.days)
			if td.days < daysdueneed:
				print "\naccount name : " + idx[1] + " will be due in less five days. Due date : " + duedate.strftime("%m/%d/%y")

class ThingsTodo(object):
	def __init__(self,task,lastdateexecute,comment):
		self.task=task
		self.lastdateexecute=lastdateexecute
		self.comment=comment
	def __str__(self):
		return (" Task to do : " + self.task + " need to do before " + self.lastdateexecute)

def enter_important_task():
	answer='no'
	while answer != 'ok':
	
		task =raw_input('\n\nenter important Task to do(q or Q to exit): ')
		if task in 'qQ':
			exit(0)
		else:	
			#task=raw_input('enter task to do : ')
			lastdateexecute=raw_input('enter task has to be done: ')
			comment=raw_input('comment : ')
			answer=raw_input('Enter ok if data is ok  :')
		
	thingstodo=ThingsTodo(task,lastdateexecute,comment)
	#print ("you entered" + account_name + owner + duedate + apr + balance + logname + pwd )
	Insert_TaskTable(task,lastdateexecute,comment)
	return  task


def Insert_TaskTable(task,lastdateexecute,comment):
	
	# prepare a cursor object using cursor() method
	cursor = db.cursor()
	
	sql = "Insert into thingstodo(task,lastdatetobedone,comment) values (%s,%s,%s)"
	args = (task,lastdateexecute,comment)
	print ('in insert task table function')
	try:
		# Execute the SQL command
		print "insert execute completed"
		cursor.execute(sql,args)
		result = cursor.fetchall()
		print result
		print "insert execute completed"
		# Commit your changes in the database
		db.commit()	
		# Rollback in case there is any error
	except MySQLdb.Error as e:
		#if e[0]!= ###:
		raise
		db.rollback()

		# disconnect from server
	db.close()
	
def Query_TaskTable(task):
	# prepare a cursor object using cursor() method
	global query_all_list
	cursor = db.cursor()
	if task=='all':
		sql = "Select * from thingstodo "
	else:
		sql = "Select * from thingstodo where task=%s "
		args = task
	#print ('in select account table function for accountname '+args)
	try:
	
		# Execute the SQL command
		#print "select execute completed"
		if task == 'all':
			noofrows=cursor.execute(sql)
			#print(noofrows)
		else:
			print "in query "
			noofrows=cursor.execute(sql,[args])
			#print(noofrows)
		
		desc = cursor.description
		#print "%-2s %-17s %-10s %-10s %-20s %-10s %-10s" % (desc[0][0].strip(), desc[1][0].strip(), desc[2][0].strip(), desc[3][0].strip(), desc[4][0], desc[5][0], desc[6][0])
		#print (desc[0][0].center(2) +  desc[1][0].center(20) + desc[2][0].center(20) + desc[3][0].center(10) +  desc[4][0].center(20) + desc[5][0].center(10)+ str(desc[6][0]).center(10))
		print (desc[0][0].rjust(2) +  desc[1][0].rjust(20) + desc[2][0].rjust(20) + desc[3][0].rjust(4) )
		print "\n=========================================================================================\n"
		for row in cursor.fetchall():
			task=row[0]
			lastdatetobedone=row[1]
			comment = row[2]
			id = str(row[3])
			#print (str(id).center(2) +  account_name.center(20) + account_type.center(20) + owner.center(10) +  duedate.center(20) + apr.center(10) + str(balance).center(5))
			print (task.rjust(2) +  lastdatetobedone.rjust(20) + comment.rjust(20) + id.rjust(4) )
			query_all_list.append(row)
	except MySQLdb.Error as e:
		print(e)
			
	#db.close()
	#print('Account_Name :' + account_name + '\nOwner \nduedate : ' + duedate + '\nAPR :' + apr + '\nBalance :' + str(balance))
	
def Delete_TaskTable(taskid):

	cursor = db.cursor()
	sql = "Delete from thingstodo where id=%s"
	args = (taskid)
	print ('in delete thingstodo table function for taskid ' + taskid)
	try:
		# Execute the SQL command
		print " in delete execute "
		cursor.execute(sql,[args])
		result = cursor.fetchall()
		for res in result:
			print str(res)
		print "delete execute completed"
		# Commit your changes in the database
		db.commit()	
		# Rollback in case there is any error
	except MySQLdb.Error as e:
		#if e[0]!= ###:
		raise
		db.rollback()
	db.close()
		
	
	
				
def usage():
	print "\n -h for help "
	print " -q account_name for query an account"
	print " -R for query all account"
	print " -d acoount_name for deleting an account"
	print " -a for adding an account"
	print " -U account_name  -> update an account column"
	print " -D find account due in 5 days from today"
	print " -T add things to do"
	print " -t show  things to do"
	print " -e delete a task table "
	
def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hq:Rd:aU:DTte:")
	except getopt.GetoptError as err:
		print str(err) 
		usage()
		sys.exit(2)
		
	
	#queryaccount= None
	#Sdeleteaccount= None
	queryall=False
	addingaccount=False
	addingaccount=False
	addingaccount=False
	
	
	for o, a in opts:
		if o == "-h":
			usage()
			sys.exit(0)
		if o == "-q":
			queryaccount=a
			Query_AccountTable(a)
			#sys.exit(0)
		elif o == "-a":
			addingaccount=True
			enter_account_info()
		elif o == "-d":
			deleteaccount=a
			Delete_Account(a)
		elif o == "-R":
			queryall=True
			Query_AccountTable('all')
		elif o == "-U":
			get_whattoupdate(a)	
		elif o == "-D":
			getaccount_due_soon()
		elif o == "-T":
			enter_important_task()
		elif o == "-t":
			Query_TaskTable('all')
		elif o == "-e":
			Delete_TaskTable(a)
		else:
			assert False, "unhandled option"
		 
		#lif o == "-aor
		#adding account=true
		#	adding account=true
        #else:
        #    assert False, "unhandled option"

#column_list('account')
if __name__ == "__main__":
    main()


#Connect_AccountInfoDB();
#account=enter_account_info()
#query_account_info()
#account.printattr()
#Delete_Account('s')