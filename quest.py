import json

FINISHED = 'completed'
ON_PROGRESS = 'on course'
TO_START = 'to start'
EXPIRED = 'time expired'
ARCHIVED = 'archived'


def is_after(date_a, date_b):
    if date_a[2] > date_b[2]:
        return True
    elif date_a[2] == date_b[2]:
        if date_a[1] > date_b[1]:
            return True
        elif date_a[1] == date_b[1]:
            if date_a[0] > date_b[0]:
                return True
    return False


def to_num_list(table):
    new_table = []
    for element in table:
        new_table.append(int(element))
    return new_table


class Quest:
    def __init__(self, dict):
        self.data = dict
        '''Dict must have at least:
            -name
            -id
            -creation_date
            -limit_date
            -description
            -status
            -priority
            -is_daily'''

    def to_json_string(self):
        return json.dumps(self.data)

    def change_status(self, new_status):
        self.data['status'] = new_status

    def rename(self, name):
        self.data['name'] = name

    def update_status(self, current_date):
        if self.getStatus() == ARCHIVED:
            return
        if not self.data['is_daily']:
            if self.data['status'] != FINISHED:
                limit_date = self.data['limit_date']
                if is_after(current_date, limit_date):
                    self.change_status(EXPIRED)
        else:
            limit_date = self.data['limit_date']
            if is_after(current_date, limit_date):
                self.change_status(TO_START)
                self.data['limit_date'] = current_date

    def set_is_daily(self, new_status):
        self.data['is_daily'] = new_status

    def complete(self):
        self.change_status(FINISHED)
        if self.isDaily():
            self.data['times_completed'] += 1

    # Getters
    def getName(self):
        return self.data['name']

    def getId(self):
        return self.data['id']

    def getCreationDate(self):
        return self.data['creation_date']

    def getLimitDate(self):
        return self.data['limit_date']

    def getDescription(self):
        return self.data['description']

    def getStatus(self):
        return self.data['status']

    def getPriority(self):
        return self.data['priority']

    def isDaily(self):
        return self.data['is_daily']

    def getTimesCompleted(self):
        if self.isDaily():
            return self.data['times_completed']
        else:
            return -1
