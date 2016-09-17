import os
from difflib import Differ, SequenceMatcher
from pgrader.merge import read_notebook


def extract_source(filename):

    result = {}
    nb = read_notebook(filename)
    for cell in nb.cells:
        metadata = cell['metadata']
        if 'nbgrader' in metadata and metadata['nbgrader']['solution']:
            grade_id = metadata['nbgrader']['grade_id']
            result[grade_id] = cell['source'].split('\n')

    return result


def extract_solution_diff(source, solution):

    d = Differ()

    result = {}
    for grade_id in source:
        diff = d.compare(source[grade_id], solution[grade_id])
        delta = ' '.join(i[2:] for i in diff if i.startswith('+ '))
        result[grade_id] = delta

    return delta


def get_src_path(course_id, assignment_id):

    return os.path.join("source", course_id, assignment_id)


def get_sol_path(user, assignment_id):

    return os.path.join("submitted", user, assignment_id)


def get_notebook_names(course_id, assignment_id):

    src_path = get_src_path(course_id, assignment_id)
    notebooks = [i for i in os.listdir(src_path) if i.endswith('ipynb')]
    return notebooks


def get_solutions(users, course_id, assignment_id):

    src_path = get_src_path(course_id, assignment_id)
    notebooks = get_notebook_names(course_id, assignment_id)

    result = {}
    for user in users:
        for notebook in notebooks:
            sol_path = get_sol_path(user, assignment_id)
            src = extract_source(os.path.join(src_path, notebook))
            sol = extract_source(os.path.join(sol_path, notebook))
            result[user] = extract_solution_diff(src, sol)

    return result


def compare_notebooks(users, course_id, assignment_id, min_ratio=0.9):


    score = []
    solutions = get_solutions(users, course_id, assignment_id)

    for i, user in enumerate(sorted(users)):
        peers = sorted(users) # make a copy
        for peer in peers[i+1:]:
            if solutions[user].strip() and solutions[peer].strip():
                matcher = SequenceMatcher(None, solutions[user], solutions[peer])
                score.append((user, peer, matcher.ratio()))

    result = [i for i in score if i[2] >= min_ratio]
    result = sorted(result, key=lambda x: x[2], reverse=True)

    return result