from .plan import Plan

def print_plans(plans):
    for i, plan in enumerate(plans):
        print(f"> Plan {i}")
        print(plan.__str__())

def print_plan(plan):
    print(plan.__str__())