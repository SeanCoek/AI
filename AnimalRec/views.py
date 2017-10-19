from django.shortcuts import render
from django.http import JsonResponse
import os

from AI.utils import utils
from AI.utils.utils import Rule


# Create your views here.
def home(request):
    return render(request, 'home.html')


def index(request):
    conditions = utils.loadCondition()
    return render(request, 'index.html', {'conditions': conditions})


def rule_add(request):
    file = open(os.path.join(os.path.dirname(os.path.dirname(__name__)), 'static', 'dict2.txt'), 'a+', encoding='utf-8')
    file.seek(0)
    words = file.readlines()
    # words = map(lambda x: x.split(':')[1], words)
    conditions = filter(lambda x: x.split(':')[0] == 'base' or x.split(':')[0] == 'middle', words)
    conditions = utils.word_prefix_cut(conditions)
    results = filter(lambda x: x.split(':')[0] == 'result' or x.split(':')[0] == 'middle', words)
    results = utils.word_prefix_cut(results)
    file.close()
    return render(request, 'rule_add.html', {'conditions': conditions, 'results': results, })


def animal_rec(request):
    rule_set, results = load()
    facts = request.POST.getlist('facts')
    process_rules = []
    process_result = None
    fact_arr_for_return = [list(facts)]
    facts_return, rules, result = utils.rec(facts, rule_set, results, process_rules, process_result, fact_arr_for_return)
    print(rules)
    return JsonResponse({'rules': rules,
                         'result': result,
                         'facts': facts_return})





def load():

    file = open(os.path.join(os.path.dirname(os.path.dirname(__name__)), 'static', 'rule.txt'), 'r', encoding='utf-8')
    file_lines = file.readlines()
    file_lines = map(lambda x: x.split(':')[1], file_lines)
    rule_set = map(lambda x: Rule(x.split('->')[0], x.split('->')[1]), file_lines)
    rule_set = list(rule_set)
    file.close()
    file = open(os.path.join(os.path.dirname(os.path.dirname(__name__)), 'static', 'dict2.txt'), 'r', encoding='utf-8')
    file_lines = file.readlines()
    results = filter(lambda x: x.split(':')[0] == 'result', file_lines)
    results = map(lambda x: x.split(':')[1], results)
    results = map(lambda x: x.replace('\n', ''), results)
    results = list(results)
    file.close()
    return rule_set, results