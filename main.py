import json, sys
import quest as Qst
from datetime import date


def status_points(quest):
    status = quest.getStatus()
    if status == Qst.ON_PROGRESS:
        return 1
    elif status == Qst.TO_START:
        return 2
    elif status == Qst.ARCHIVED:
        return 2.5
    elif status == Qst.EXPIRED:
        return 3
    elif status == Qst.FINISHED:
        return 4


def get_priority(quest):
    return quest.getPriority()


def get_id(quest):
    return quest.getId()


def read_quests(path):
    quests_list = []
    file_content = open(path).read()
    quests_data = json.loads(file_content)
    for quest in quests_data:
        quests_list.append(Qst.Quest(quests_data[quest]))
    return quests_list


def save_quests(path):
    with open(path, 'w') as file:
        content = '{\n'
        for quest in quest_list:
            content += f'\t"q_{quest.getId()}": '
            content += quest.to_json_string()
            if quest is not quest_list[len(quest_list) - 1]:
                content += ','
            content += '\n'
        content += '}'
        file.write(content)


def get_higher_id():
    ids = []
    for quest in quest_list:
        ids.append(quest.getId())
    return max(ids)


def add_quest(**kwargs):
    new_quest = Qst.Quest({
        'name': kwargs['NAME'],
        'description': kwargs['DESCRIPTION'],
        'creation_date': to_num_list(date.today().strftime("%d-%m-%y").split('-')),
        'limit_date': kwargs['LIMIT_DATE'],
        'id': get_higher_id()+1,
        'status': Qst.TO_START,
        'priority': kwargs['PRIORITY'],
        'is_daily': kwargs['IS_DAILY'],
        'times_completed': 0,
        'seu novo atributo': 0
    })
    quest_list.append(new_quest)


def ask_for_new_quest():
    print('Adding a new quest to the Quest Board...')
    # Asks all the information to the user
    name = input("Quest's Name: ").strip()
    limit_date = to_num_list(input("Quest's End Date (dd-mm-yy): ").strip().split('-'))
    desc = input("Quest's Description: ").strip()
    priority = int(input("Quest's Priority: ").strip())
    daily_answer = input("Is it daily? [s/n]: ").lower().strip()
    # Configures the Is_Daily
    is_daily = False
    if daily_answer == 's':
        is_daily = True
    # Adds the quest
    add_quest(NAME=name, DESCRIPTION=desc, LIMIT_DATE=limit_date, PRIORITY=priority, IS_DAILY=is_daily)
    print(f'Successfully added the new quest: {name}')


def list_quests(args):
    show = {'completed': False,
            'expired': False,
            'archived': False,
            'all': False}
    if args.count('--status') > 0:
        quest_list.sort(key=status_points)
    elif args.count('--priority') > 0:
        quest_list.sort(key=get_priority)
        quest_list.reverse()
    elif args.count('--id') > 0:
        quest_list.sort(key=get_id)
    if args.count('--show-completed') > 0:
        show['completed'] = True
    if args.count('--show-expired') > 0:
        show['expired'] = True
    if args.count('--show-archived') > 0:
        show['archived'] = True
    if args.count('--show-all') > 0:
        show['all'] = True
    print('Current quests:')

    for quest in quest_list:
        if not show['all']:
            if quest.getStatus() == Qst.FINISHED and not show['completed']:
                continue
            if quest.getStatus() == Qst.EXPIRED and not show['expired']:
                continue
            if quest.getStatus() == Qst.ARCHIVED and not show['archived']:
               continue

        if quest.isDaily():
            daily_text = '*'
        else:
            daily_text = ' '
        print(' '*(5 - len(str(quest.getId()))) + f'{quest.getId()}.{daily_text}\t{quest.getName()}\tSTATUS: {quest.getStatus()}\tPRIORITY: {quest.getPriority()}\tEnd: {date_list_to_str(quest.getLimitDate())}')


def del_quest(search_word, mode):
    if mode == 'name':
        for quest in quest_list:
            if quest.getName() == search_word:
                quest_list.remove(quest)
                break
    elif mode == 'id':
        for quest in quest_list:
            if quest.getId() == int(search_word):
                quest_list.remove(quest)
                break


def update_status(quest, new_status):
    quest.change_status(new_status)


def show_quest(quest):
    width = 36
    if quest.isDaily():
        daily_text = ' | DAILY'
        times_comp_text = f' x {quest.getTimesCompleted()}'
    else:
        daily_text = ''
        times_comp_text = ''
    print('@'+'-'*width)
    print(f'|{quest.getName()} | Priority: {quest.getPriority()}')
    print(f'|From: {date_list_to_str(quest.getCreationDate())} Until: {date_list_to_str(quest.getLimitDate())}')
    print(f'|Status: {quest.getStatus()} | ID: {quest.getId()}{daily_text}{times_comp_text}')
    print('@'+'-'*width)
    print(f'Description: {quest.getDescription()}')


def to_num_list(table):
    new_table = []
    for element in table:
        new_table.append(int(element))
    return new_table


def date_list_to_str(date_list):
    day = str(date_list[0])
    month = str(date_list[1])
    year = str(date_list[2])
    # Places a 0 in front of the numbers if they are one digit
    if len(day) < 2:
        day = '0' + day
    if len(month) < 2:
        month = '0' + month
    if len(year) < 2:
        year = '0' + year
    return f'{day}-{month}-{year}'


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


def update_all_quests_statuses():
    current_date = to_num_list(str(date.today().strftime("%d-%m-%y")).split('-'))
    for quest in quest_list:
        quest.update_status(current_date)


def rename(quest, name):
    quest.rename(name)


def to_daily(quest, status):
    quest.set_is_daily(status)


def rest_daily(quest):
    if quest.isDaily():
        quest.change_status(Qst.ARCHIVED)
    else:
        print('Quest is not daily and can\'t be archived')


def unrest_daily(quest):
    if quest.isDaily():
        quest.change_status(Qst.TO_START)
    else:
        print('Quest is not daily and can\'t be archived')


PATH = 'quest_list.json'
quest_list = read_quests(PATH)


def main(argv):
    for i in range(len(argv)):
        if argv[i] == '-l':
            list_quests(argv)
        elif argv[i] == '-a':
            ask_for_new_quest()
        elif argv[i] == '-d':
            del_quest(argv[i+1], 'id')
            i += 2
        elif argv[i] == '-show':
            for quest in quest_list:
                if quest.getId() == int(argv[i+1]):
                    show_quest(quest)
                    break
        elif argv[i] == '-start':
            for quest in quest_list:
                if quest.getId() == int(argv[i+1]):
                    update_status(quest, Qst.ON_PROGRESS)
                    break
        elif argv[i] == '-complete':
            for quest in quest_list:
                if quest.getId() == int(argv[i+1]):
                    quest.complete()
                    break
        elif argv[i] == '-rename':
            for quest in quest_list:
                if quest.getId() == int(argv[i+1]):
                    rename(quest, argv[i+2])
                    break
        elif argv[i] == '-yes-daily':
            for quest in quest_list:
                if quest.getId() == int(argv[i+1]):
                    to_daily(quest, True)
                    break
        elif argv[i] == '-no-daily':
            for quest in quest_list:
                if quest.getId() == int(argv[i+1]):
                    to_daily(quest, False)
                    break        
        elif argv[i] == '-rest-daily':
            for quest in quest_list:
                if quest.getId() == int(argv[i+1]):
                    rest_daily(quest)
                    break
        elif argv[i] == '-unrest-daily':
            for quest in quest_list:
                if quest.getId() == int(argv[i+1]):
                    unrest_daily(quest)
                    break
    save_quests(PATH)


if __name__ == '__main__':
    update_all_quests_statuses()
    main(sys.argv)
