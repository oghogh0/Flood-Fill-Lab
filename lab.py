"""
6.1010 Spring '23 Lab 4: Recipes
"""

import pickle
import sys

sys.setrecursionlimit(20_000)
# NO ADDITIONAL IMPORTS!


def make_recipe_book(recipes):
    """
    Given recipes, a list containing compound and atomic food items, make and
    return a dictionary that maps each compound food item name to a list
    of all the ingredient lists associated with that name.
    """
    compound_recipe = {}

    for compound in recipes:
        if compound[0] == "compound":
            if compound[1] not in compound_recipe:
                compound_recipe[compound[1]] = [compound[2]]
            else:
                compound_recipe[compound[1]].append(compound[2])

    return compound_recipe


def make_atomic_costs(recipes):
    """
    Given a recipes list, make and return a dictionary mapping each atomic food item
    name to its cost.
    """
    atomic_recipe = {}

    for atomic in recipes:
        if atomic[0] == "atomic":
            atomic_recipe[atomic[1]] = atomic[2]

    return atomic_recipe


def lowest_cost(recipes, food_item, forbidden = []):
    """
    Given a recipes list and the name of a food item, return the lowest cost of
    a full recipe for the given food item.
    """
    recipe_book =  make_recipe_book(recipes)
    atomic_costs = make_atomic_costs(recipes)
    
    if food_item not in recipe_book and food_item not in atomic_costs:
        return None

    elif food_item in forbidden:  # check if atomic item in forbidden list (base case)
        return None

    elif food_item in atomic_costs:  # base case is atomic item - all compound made of atomic
        return atomic_costs[food_item]

    else:
        result = []

        for variant in recipe_book[food_item]:
            ingredients = []  # list of lowest cost of making each item

            for item in variant:
                low = lowest_cost(
                    recipes, item[0], forbidden
                )  # assume lowest_cost works, make sure to pass forbidden
                if low is not None:  # 1 variant fails
                    ingredients.append(low * item[1])
                else:
                    ingredients.append("None")

            if "None" in ingredients:  # ignore
                continue
            else:
                tot = sum(ingredients)
                result.append(tot)

        if not result:  # all variants don't work , result == []
            return None
        else:
            min_cost = min(result)

    return min_cost


def scale_recipe(flat_recipe, n):
    """
    Given a dictionary of ingredients mapped to quantities needed, returns a
    new dictionary with the quantities scaled by n.
    """
    scaled_flat_recipe = {}

    for item in flat_recipe:
        scaled_flat_recipe[item] = flat_recipe[item] * n

    return scaled_flat_recipe


def make_grocery_list(flat_recipes):
    """
    Given a list of flat_recipe dictionaries that map food items to quantities,
    return a new overall 'grocery list' dictionary that maps each ingredient name
    to the sum of its quantities across the given flat recipes.

    For example,
        make_grocery_list([{'milk':1, 'chocolate':1}, {'sugar':1, 'milk':2}])
    should return:
        {'milk':3, 'chocolate': 1, 'sugar': 1}
    """
    grocery_list = {}

    for flat in flat_recipes:
        for item in flat:
            if item not in grocery_list:
                grocery_list[item] = flat[item]
            else:
                grocery_list[item] += flat[item]

    return grocery_list


def flat_recipe_cost(recipes, flat_recipe):
    """
    Returns cost of items in flat_recipe
    """
    sum_cost = []
    for item in flat_recipe:
        cost = flat_recipe[item] * make_atomic_costs(recipes)[item]
        sum_cost.append(cost)

    return sum(sum_cost)


def cheapest_flat_recipe(recipes, food_item, forbidden=[]):
    """
    Given a recipes list and the name of a food item, return a dictionary
    (mapping atomic food items to quantities) representing the cheapest full
    recipe for the given food item.

    Returns None if there is no possible recipe.
    """
    recipe_book =  make_recipe_book(recipes)
    atomic_costs = make_atomic_costs(recipes)

    flat_recipe_dict = {}

    if food_item not in recipe_book and food_item not in atomic_costs:
        return None

    elif food_item in forbidden:  # check if atomic item in forbidden list (base case)
        return None

    elif food_item in atomic_costs:
        flat_recipe_dict[food_item] = 1  # base case quantity is 1
        return flat_recipe_dict

    else:
        result = []

        for variant in recipe_book[food_item]:
            ingredients = []

            for item in variant:
                flat_item_recipe = cheapest_flat_recipe(
                    recipes, item[0], forbidden
                )  # cheapest flat recipe of each item
                if flat_item_recipe is not None:
                    scaled_flat_item_recipe = scale_recipe(
                        flat_item_recipe, item[1]
                    )  # scale it by quantity
                    ingredients.append(scaled_flat_item_recipe)
                else:
                    ingredients.append("None")
            if "None" in ingredients:  # ignore
                continue
            else:
                grocery_list = make_grocery_list(
                    ingredients
                )  # make grocery list of all dicts
                result.append(grocery_list)  # list of grocery_list of diff variants

    if not result:  # all variants don't work
        return None

    else:
        min_recipe = ["None", float("inf")]

        for recipe in result:
            recipe_cost = flat_recipe_cost(recipes, recipe)  # cost
            if recipe_cost < min_recipe[1]:
                min_recipe = [recipe, recipe_cost]

        return min_recipe[0]


def ingredient_mixes(flat_recipes):
    """
    Given a list of lists of dictionaries, where each inner list represents all
    the flat recipes make a certain ingredient as part of a recipe, compute all
    combinations of the flat recipes.
    """
    if len(flat_recipes) == 1:
        return flat_recipes[0]

    else:
        mix_list = []
        mixture = ingredient_mixes(flat_recipes[1:])  # other flat recipes

        for flat_recipe in flat_recipes[0]:
            flat_copy = flat_recipe.copy()  # list of dict

            for mix in mixture:
                new_recipe = make_grocery_list(
                    [flat_copy, mix])  # helps find total e.g. pb twice (no update bc mutates)
                mix_list.append(new_recipe)

    return mix_list


def all_flat_recipes(recipes, food_item, forbidden=[]):
    """
    Given a list of recipes and the name of a food item, produce a list (in any
    order) of all possible flat recipes for that category.

    Returns an empty list if there are no possible recipes
    """
    recipe_book = make_recipe_book(recipes)
    atomic_costs = make_atomic_costs(recipes)

    if food_item not in recipe_book and food_item not in atomic_costs:
        return []

    elif food_item in forbidden:  # check if atomic item in forbidden list (base case)
        return []

    elif food_item in atomic_costs:
        return [{food_item: 1}]

    else:
        flat_recipe_list = []

        for variant in recipe_book[food_item]:  # each variant
            all_scaled_flat_list = []  # particular to each recipe

            for item, quantity in variant:
                flat_item = all_flat_recipes(recipes, item, forbidden)

                scaled_flat_list = []

                for flat_dict in flat_item: #if forbidden, flat_item = []
                    scaled_flat_item = scale_recipe(
                        flat_dict, quantity)  # scale each dict
                    scaled_flat_list.append(scaled_flat_item)
                
                all_scaled_flat_list.append(scaled_flat_list)

            
            ingredient_mixture = ingredient_mixes(all_scaled_flat_list)
            flat_recipe_list.extend(ingredient_mixture)

    return flat_recipe_list


if __name__ == "__main__":
    # load example recipes from section 3 of the write-up
    with open("test_recipes/example_recipes.pickle", "rb") as f:
        example_recipes = pickle.load(f)
    # for i in all_flat_recipes(example_recipes, "burger"):
    #     print(i)

    # print(example_recipes)
    # print(sum(make_atomic_costs(example_recipes).values()))

    # count = 0
    # for i in make_recipe_book(example_recipes):
    #     if len(make_recipe_book(example_recipes)[i]) > 1:
    #         count+=1
    # print(count)

    # dairy_recipes = [
    #     ("compound", "milk", [("cow", 2), ("milking stool", 1)]),
    #     ("compound", "cheese", [("milk", 1), ("time", 1)]),
    #     ("compound", "cheese", [("cutting-edge laboratory", 11)]),
    #     ("atomic", "milking stool", 5),
    #     ("atomic", "cutting-edge laboratory", 1000),
    #     ("atomic", "time", 10000),
    #     ("atomic", "cow", 100),
    # ]
    # print(cheapest_flat_recipe(dairy_recipes, 'cheese'))
    # print(make_recipe_book(dairy_recipes))

    # cookie_recipes = [
    #     ("compound", "cookie sandwich", [("cookie", 2), ("ice cream scoop", 3)]),
    #     ("compound", "cookie", [("chocolate chips", 3)]),
    #     ("compound", "cookie", [("sugar", 10)]),
    #     ("atomic", "chocolate chips", 200),
    #     ("atomic", "sugar", 5),
    #     ("compound", "ice cream scoop", [("vanilla ice cream", 1)]),
    #     ("compound", "ice cream scoop", [("chocolate ice cream", 1)]),
    #     ("atomic", "vanilla ice cream", 20),
    #     ("atomic", "chocolate ice cream", 30),
    # ]

    # print(make_recipe_book(cookie_recipes))
    # print(make_atomic_costs(cookie_recipes))
    # print(lowest_cost(cookie_recipes, "milk"))

#     dairy_recipes_2 = [
#     ('compound', 'milk', [('cow', 2), ('milking stool', 1)]),
#     ('compound', 'cheese', [('milk', 1), ('time', 1)]),
#     ('compound', 'cheese', [('cutting-edge laboratory', 11)]),
#     ('atomic', 'milking stool', 5),
#     ('atomic', 'cutting-edge laboratory', 1000),
#     ('atomic', 'time', 10000),
# ]
#     print(lowest_cost(dairy_recipes_2, 'cheese'))

# print(make_grocery_list([{'milk':1, 'chocolate':1}, {'sugar':1, 'milk':2}]))

# print((ingredient_mixes(
#     [[{'peanut butter': 1}, {'almond butter': 1}, {'butter':3}],
#     [{'jelly': 2}, {'bread':4}]]
# )))
