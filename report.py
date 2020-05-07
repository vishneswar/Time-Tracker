import json
import pprint as p
import datetime as dt
import os
import sys

def report(date_str):
    """Generate the usage report for the specified date"""
    try:
        with open(os.path.join(date_str, 'timetracker.json'), 'r') as file:
            data = json.load(file)
            utilization_report = {}
            for activity in data['activities']:
                utilization_report.setdefault(activity['event'], '0:00:00')
                for log in activity['log']:
                    try:
                        total_time = add_time(utilization_report[activity['event']], log['duration']) 
                        utilization_report[activity['event']] = total_time
                    except:
                        pass
            print()
            print("Complete Data".center(100, '-'))
            print()
            print('TASK'.rjust(45, ' '), end='')
            print('  |  TIME Spent\n')
            for key, val in utilization_report.items():
                if len(key) > 40:
                    key = key[len(key) - 40: len(key)]
                    key = '...' + key
                print(key.rjust(45, ' '), end='')
                print("  |  ", val)
            print()
            print("Important Data".center(100, '-'))
            print()
            print('TASK'.rjust(45, ' '), end='')
            print('  |  TIME Spent\n')
            wanted_list = ['Visual Studio Code', 'Sublime Text', 'Excel', 'Google Chrome', 'terminal', 'Desktop', 'Notepad', 'Outlook', 'Eclipse']
            for ele in wanted_list:
                print(ele.rjust(45, ' '), end='')
                try:
                    print("  |  ", utilization_report[ele])
                except:
                    print("  |  ", 'No data available')
    except FileNotFoundError:
        print('Data not available for the specified date')
    except Exception as e:
        print("Error processing the date", e)

        
def add_time(a, b):
    a = a.split(':')
    b = b.split(':')
    c = [0,0,0]
    for i in range(3):
        c[i] = int(a[i]) + int(b[i])
        if c[i] > 60 and i > 0:
            c[i - 1] = int(c[i -1]) + c[i] // 60
            c[i] = c[i] % 60
            if c[i - 1] < 10:
                c[i - 1] = '0' + str(c[i - 1])
            else:
                c[i - 1] = str(c[i - 1])
        if c[i] < 10:
            c[i] = '0' + str(c[i])
        else:
            c[i] = str(c[i])

    sum = ':'.join(c)
    return sum


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'USAGE: python {sys.argv[0]} <YYYY-MM-DD>')
    else:
        report(sys.argv[1])