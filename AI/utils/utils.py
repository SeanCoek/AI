import os


def filter_condition(x):
    return x == 'base' or x == 'middle'


def word_prefix_cut(list):
    return map(lambda x: x.split(':')[1], list)


class Rule(object):
    def __init__(self, condition, result, used=False):
        self.condition = condition.split('&')
        self.result = result
        self.used = used


def loadCondition():
    file = open(os.path.join(os.path.dirname(os.path.dirname(__name__)), 'static', 'dict2.txt'), 'r', encoding='utf-8')
    file_lines = file.readlines()
    conditions = filter(lambda x: x.split(':')[0] == 'base' or x.split(':')[0] == 'middle', file_lines)
    conditions = map(lambda x: x.split(':')[1], conditions)
    conditions = map(lambda x: x.replace('\n', ''), conditions)
    conditions = list(conditions)
    file.close()
    return conditions


def rec(fact, rule_set, results, process_rules, process_result, fact_arr_for_return):
    for i in range(len(fact)):
        if fact[i] in results:
            # print(fact[i])
            process_result = fact[i]
            return fact_arr_for_return, process_rules, process_result
    matchIndex = match(fact, rule_set)
    # for index in matchIndex:
    #     print(ruleSet[index].result)
    if len(matchIndex) < 1:
        # print('No result')
        process_result = None
        return fact_arr_for_return, process_rules, process_result
    for i in range(len(matchIndex)):
        print(rule_set[matchIndex[i]].result)
        if rule_set[matchIndex[i]].result in results:
            print(rule_set[matchIndex[i]].result)
            process_result = rule_set[matchIndex[i]].result
            return fact_arr_for_return, process_rules, process_result
    if len(matchIndex) > 1:
        # we got more than 1 matched rules here.
        # make a decision for which rule we should use next
        decision = collide(matchIndex, rule_set)
        fact.append(rule_set[decision].result[0:-1])
        fact_arr_for_return.append(list(fact))
        rule_set[decision].used = True
        process_rules.append('&'.join(rule_set[decision].condition) + '->' + rule_set[decision].result[0:-1])
        return rec(fact, rule_set, results, process_rules, process_result, fact_arr_for_return)
    if len(matchIndex) == 1:
        fact.append(rule_set[matchIndex[0]].result.replace('\n', ''))
        fact_arr_for_return.append(list(fact))
        rule_set[matchIndex[0]].used = True
        process_rules.append('&'.join(rule_set[matchIndex[0]].condition) + '->' + rule_set[matchIndex[0]].result[0:-1])
        return rec(fact, rule_set, results, process_rules, process_result, fact_arr_for_return)


def match(fact, result_set):
    print(fact)
    matchIndex = []
    for i in range(len(result_set)):
        if result_set[i].used:
            # rule has been used
            continue
        condition = result_set[i].condition
        exists = False
        for j in range(len(condition)):
            if condition[j] in fact:
                # condition is in fact
                exists = True
                continue
            else:
                # condition is not in fact
                exists = False
                break
        if exists:
            matchIndex.append(i)

    return matchIndex


def collide(matchIndex, rule_set):
    decision = 0
    for i in range(len(matchIndex)):
        # find the best rule we gonna use. ( here we choose rule which has more conditions )
        if len(rule_set[matchIndex[i]].condition) > len(rule_set[matchIndex[decision]].condition):
            decision = i
    return matchIndex[decision]
