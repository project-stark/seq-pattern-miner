import pymysql as pms
from datetime import datetime


def fetch_data():
        # connect with the mysql database
        conn = pms.connect(host='localhost', user='root', passwd='div3125', db='devicedata')
        sql = """SELECT * FROM dataset ORDER BY firetime"""
        cursor = conn.cursor()
        try:
            # fetch data
            cursor.execute(sql)
            data = list(cursor.fetchall())
            data_list = []
            # split single datetime element in date and time
            for row in data:
                device_name, event, timestamp = row
                data_list.append([device_name, event] + str(timestamp).split(' '))
            return data_list

        except:
            return None


def pre_process_data():
    data = fetch_data()

    # check for empty data
    if data is None:
        return None, None
    # segregate data date-wise
    else:
        processed_data = {}
        # get unique set of all available dates
        unique_dates = set(x[2] for x in data)
        # get events for each date
        for each_date in unique_dates:
            processed_data[each_date] = [[x[0], x[1], x[3]] for x in
                                         list(filter(lambda x: x[2] == each_date, data))]
        return processed_data


def find_patterns():
    data = pre_process_data()

    # check for empty data
    if data is None:
        return None
    # mine patterns for each day
    else:
        threshold_minutes = 5
        date_format = '%H:%M:%S'
        patterns = {}

        for each_record in data.keys():
            flag = False
            pattern = []
            daily_patterns = []
            for record in data[each_record][:len(data[each_record])-1]:
                r1 = record
                r2 = data[each_record][data[each_record].index(r1)+1]

                # calculate time difference between each of the consecutive events
                time_offset = (datetime.strptime(r2[2], date_format) - datetime.strptime(r1[2], date_format))

                # clause for addition to an empty list
                if int(str(time_offset).split(':')[1]) < threshold_minutes and not flag:
                    flag = True
                    pattern.append(r1[0] + ':' + r1[1])
                    pattern.append(r2[0] + ':' + r2[1])

                # clause for addition to non-empty list
                elif int(str(time_offset).split(':')[1]) < 5 and flag:
                    pattern.append(r2[0] + ':' + r2[1])

                # end of a pattern or no pattern formation
                else:
                    if pattern:
                        daily_patterns.append('=>'.join(pattern))
                        pattern = []
                        flag = False

            # assign patterns of the day
            patterns[each_record] = daily_patterns
        return patterns

# display raw patterns
detected = find_patterns()
for key in detected.keys():
    print('Date : ' + '/'.join(key.split('-')[::-1]))
    for each_pattern in detected[key]:
        print('\t' + each_pattern)
