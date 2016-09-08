import sys
import yaml

from pgrader.assign import get_users, make_table
from pgrader.autograde import inverted, get_review


def get_comments(users, assignment_id, week):

    comments = {}

    table = make_table(users, week)
    invert = inverted(table)

    for user in users:

         yaml_data = get_review(user, assignment_id)

         if yaml_data:

             for peer in yaml_data:

                 name = invert[peer]

                 if name not in comments:
                     comments[name] = {}

                 for problem in yaml_data[peer]:

                     if problem not in comments[name]:
                         comments[name][problem] = []
                     review = yaml_data[peer][problem]

                     if review["comments"]:
                         comments[name][problem].append(review["comments"])

    sys.stdout.write(yaml.dump(comments))