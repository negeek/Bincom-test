
from random import randint
from bs4 import BeautifulSoup
import psycopg2


# Below is the solution to the Test questions in "https://docs.google.com/document/d/1ik1fuc6L_Y-yIDeaJnlVBIwPeA5AvwAaciaQkHreMrM/edit"

class BincomColorPage:
    def __init__(self, path):
        self.path = path

    def web_data(self):
        html_file = open(self.path, "r")

        # Reading the file and storing in a variable
        contents = html_file.read()

        # Creating a BeautifulSoup object and
        # specifying the parser
        beautifulSoupText = BeautifulSoup(contents, 'lxml')
        raw_data = beautifulSoupText.find_all('tr')

        # creating a dictionary for days of the week
        day_dict = {0: 'MONDAY', 1: 'TUESDAY',
                    2: 'WEDNESDAY', 3: 'THURSDAY', 4: 'FRIDAY'}

        # dictionary to store the clean data
        clean_data = {}
        # loop the unprocessed data
        for day in range(len(raw_data)):
            day_idx = day
            daystr = str(raw_data[day])  # covert to str to slice it
            for ele in range(len(daystr)):
                # if td tag is encountered the next thing is the day of the week
                if daystr[ele:ele+4] == '<td>':
                    val = daystr[ele + 14 +
                                 len(day_dict[day_idx]):-11].split(',\n')
                    val_space = val[1].strip().split(', ')
                    val_space.extend(val[0].split(', '))
                    # put the day inside clean_data using its index in day_dict
                    clean_data[day_dict[day_idx]] = val_space
                    break
        return clean_data

    def color_freq_data(self):
        clean_data = self.web_data()
        suitable_data = {}
        for key, value in clean_data.items():
            suitable_data[key] = {}
            for color in value:
                try:
                    if suitable_data[key][color]:
                        suitable_data[key][color] += 1
                except KeyError:
                    suitable_data[key][color] = 1
        freq_of_colors = {}
        for day in suitable_data:
            for color in suitable_data[day].keys():
                try:
                    if freq_of_colors[color]:
                        freq_of_colors[color] += suitable_data[day][color]
                except KeyError:
                    freq_of_colors[color] = suitable_data[day][color]
        return freq_of_colors

    def mean(self):
        avg = sum(self.color_freq_data().values())/len(self.color_freq_data())
        return avg

    def mode(self):
        max_num = 0
        ans = []
        for color, freq in self.color_freq_data().items():
            if freq > max_num:
                max_num = freq
                ans.append(color)
        return ans[-1]

    def median(self):
        freqs = sorted(self.color_freq_data().values())
        if len(freqs) % 2 == 0:
            mid = (freqs[len(freqs)//2]+freqs[(len(freqs)//2)-1])/2
        else:
            mid = freqs[len(freqs)//2]
        return mid

    def variance(self):
        summ = 0
        for freq in self.color_freq_data().values():
            summ += (freq-self.mean())**2
        var = summ/len(self.color_freq_data())
        return var

    def redProb(self):
        space = sum(self.color_freq_data().values())
        prob_red = self.color_freq_data()['RED']/space
        return prob_red

    def postgres(self):
        conn = psycopg2.connect(
            database="postgres",
            user='postgres',
            password='dlion5ive',
            host='localhost',
            port='5432')

        conn.autocommit = True
        cursor = conn.cursor()

        sql = '''CREATE TABLE COLORS(color varchar(30) NOT NULL,\
                frequency int NOT NULL);'''

        cursor.execute(sql)

        color_dicts = []
        for color, freq in self.color_freq_data().items():
            color_dicts.append({'color': color, 'frequency': freq})

        cursor.executemany(
            """INSERT INTO COLORS(color,frequency) VALUES (%(color)s, %(frequency)s)""", color_dicts)


binCom = BincomColorPage("page.html")
#   QUESTION 1
print(binCom.mean())

#   QUESTION 2
print(binCom.mode())

#   QUESTION 3
print(binCom.median())

#   QUESTION 4
print(binCom.variance())

#   QUESTION 5
print(binCom.redProb())

#   QUESTION 6
print(binCom.postgres())

#   QUESTION 7


def search(myList, number):
    '''returns index of the number'''
    def search_recursive(lst, num):
        if lst[0] == num:
            return 0
        return 1 + search_recursive(lst[1:], num)
    try:
        return search_recursive(myList, number)
    except IndexError:
        return 'Not Found'


print(search([2, 3, 4, 5, 6, 7, 8, 9], 4))

#   QUESTION 8


def random0s1s():
    rand = ''
    for i in range(4):
        rand += str(randint(0, 1))
    return int(rand, 2)


print(random0s1s())


#   QUESTION 9
class fibonacci:
    def __init__(self, n):
        self.n = n

    def nthNumber(self, num):
        '''returns the nth fibonacci number'''
        if num == 1:
            return 1
        if num < 1:
            return 0
        return self.nthNumber(num-1)+self.nthNumber(num-2)

    def SumOfFirstN(self):
        '''returns sum of first n numbers in fibonacci sequence'''
        ans = 0
        for i in range(1, self.n+1):
            ans += self.nthNumber(i)
        return ans


print(fibonacci(50).SumOfFirstN())
