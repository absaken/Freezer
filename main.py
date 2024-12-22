from decimal import Decimal
from datetime import datetime
import datetime

goods = {'Фабрика №2: яйца': [{'amount': Decimal('2'),
                       'expiration_date': datetime.date(2024, 12, 19)},
                      {'amount': Decimal('3'),
                       'expiration_date': datetime.date(2024, 12, 21)}],
 'Яйца Фабрики №1': [{'amount': Decimal('1'),
                      'expiration_date': datetime.date(2024, 12, 23)}],
 'макароны': [{'amount': Decimal('100'), 'expiration_date': None}]}
def add(items, title, amount, expiration_date=None):
    if expiration_date:
        expiration_date = datetime.datetime.strptime(expiration_date, '%Y-%m-%d').date()
    if title not in items:
        items[title] = [{'amount': amount, 'expiration_date': expiration_date}]
    else:
        items[title].append({'amount': amount, 'expiration_date': expiration_date})

def add_by_note(items, note):
    split_string = note.split()
    if split_string[-1].split('-') and len(split_string[-1].split('-')) == 3:
        add_date = split_string[-1]
        add_quantity = split_string[-2]
        split_string = split_string[:-2]
        if len(split_string) > 0:
            split_string = ' '.join(split_string)
        add(items, split_string, Decimal(add_quantity), add_date)
    else:
        add_quantity = split_string[-1]
        split_string.remove(add_quantity)
        if len(split_string) > 0:
            split_string = ' '.join(split_string)
        add(items, split_string, Decimal(add_quantity))

def find(items, needle):
    needle = needle.lower()
    return [key for key in items if needle in key.lower()]

def get_amount(items, needle):
    n = find(items, needle)
    if len(n) == 1:
        n = needle.lower()
        for item in items:
            if item.lower() == n:
                if len(items[item]) > 1:
                    return sum(item['amount'] for item in items[item])
                else:
                    return items[item][0]['amount']
    else:
        total = Decimal('0')
        for i in n:
            i = i.lower()
            for item in items:
                if item.lower() == i:
                    if len(items[item]) > 1:
                        total += sum(item['amount'] for item in items[item])
                    else:
                        total += items[item][0]['amount']
        return total

def get_expired(items, in_advance_days=0):
    expired_items = []
    if in_advance_days is None:
        in_advance_days = 0
    if in_advance_days == 0 or in_advance_days is None or in_advance_days == 'in_advance_days=None' or in_advance_days == 'None':
        day = datetime.date.today()
    else:
        day = datetime.date.today() + datetime.timedelta(days=in_advance_days)
    for item, details in items.items():
        for detail in details:
            if detail['expiration_date'] is not None and detail['expiration_date'] <= day:
                if not expired_items:
                    expired_items.append((item, detail['amount']))
                else:
                    found = False
                    for i in range(len(expired_items)):
                        if expired_items[i][0] == item:
                            expired_items[i] = (item, expired_items[i][1] + detail['amount'])
                            found = True
                            break
                    if not found:
                        expired_items.append((item, detail['amount']))
    return expired_items
print(get_expired(goods, None))