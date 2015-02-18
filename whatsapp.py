
import pandas as pd
import numpy as np
import codecs
import csv


# downloaded file have lines with the following format:
# mm/dd/yr hh:mm:ss AM/PM : user_name: msg
# when a user joins, leaves or changes the subject of group
# it is indicated as "user joined", "user left" or "user changed the subject"

#processing text
# first use sed commands to get rid of lines indicating users have joined, left or changed the group subject
# for example sed -i '/joined/d' filename

f=codecs.open('chats.txt', encoding='utf-8') # file is encoded in utf-8 format

time = []
user = []
msgs = []

for line in f:
   line = line.encode('ascii', errors='ignore') # keeping ascii characters 
   s=line.split('M:') # split line with delimiter as 'M:' to grab timestamp
    
   if(len(s)>1):
       time.append(s[0]+'M')
       ssplit = s[1].split(':') #further split to grab username and messages
   else:
       continue
   user.append(ssplit[0])
   msgs.append(ssplit[1:])
f.close()

# if you want to export data to a csv file you can use the following lines

g = open("chats.csv",'wb')
wr = csv.writer(g, dialect='excel')

wr.writerow(['time','user','msgs']) 
for i in range(0,len(time)):
  temp = [time[i],user[i],msgs[i]]
  wr.writerow(temp)
g.close()

#reading dataframe using pandas 
df = pd.read_csv('chats.csv', date_parser='time')
# once you have the dataframe you can analyze this data to get interesting 
#insights, I do some exploratory analysis here


### Usage per week

#converting to datetime
df['time_new']= pd.to_datetime(df.time)

#determining week of the year based on dates 
df['weekofyear']=df['time_new'].apply(lambda x: x.weekofyear)
df['weekofyear']=df['weekofyear'].apply(lambda x: x-df.weekofyear.min()+1)

#counting how many messages recorded every week
weekofyear = df.groupby('weekofyear').count()

plt.figure(1)
weekofyear.plot(weekofyear.index,'msgs', kind='bar',color='r',alpha=0.4)
plt.xlabel('Age of group (in weeks)')
plt.ylabel('Total number of group msgs each week')
plt.xlim(xmax=13)
plt.savefig('age.png')


### Hourly usage

def part_of_day(s):
    return s.time().hour

df['part_of_day'] = df['time_new'].map(part_of_day)
prt_day = df.groupby('part_of_day').count()

plt.figure(2)
prt_day.plot(x=prt_day.index,y='msgs', kind='bar',alpha=0.4)
plt.ylabel('Total number of chats each hour of the day')
plt.xlabel('Day Hours')
plt.savefig('hours.png')


### Weekly usage

df['day']=df['time_new'].apply(lambda x: str(x.date().weekday()))

dd = {'0':'Monday','1':'Tuesday','2':'Wednesday','3':'Thursday','4':'Friday','5':'Saturday','6':'Sunday'}

df['day']=df.day.map(dd)
day=df.groupby('day').count().sort(['msgs'],ascending=0)

plt.figure(3)
day.plot(day.index,'msgs',kind='bar',color='g',alpha=0.4)
plt.xlabel('Weekday')
plt.ylabel('Number of chats')
plt.xticks(rotation='20')
plt.savefig('weekday.png')


### User based usage

user_count = df.groupby('user').count()
user_count = user_count.sort(['msgs'],ascending = 0)

plt.figure(4)
user_count.plot(x=user_count.index,y='msgs',kind='bar',alpha=0.4,color='m')
plt.ylabel('Number of Texts')

