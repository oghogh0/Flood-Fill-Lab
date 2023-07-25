<h1>Recipes Lab</h1>
<h2>Description</h2>
We are given a list of food items. Some are "atomic" - they are not comprised of other items and are represented as a tuple of three elements: the word "atomic", a name, and a cost e.g. ('atomic', 'jalapeño pepper', 0.15). Some are "compound" -  they are created by combining other food items and are represented as a tuple of three elements: the word "compound" & their last element is an ingredient list. Ingredient list is a list of tuples, each containing an ingredient (any food item) & an int of how much of that ingredient is required to prepare the recipe e.g.  ('compound', 'spicy chili', [('can of beans', 3), ('jalapeño pepper', 10), ('chili powder', 1), ('cornbread', 2)]). It is important to note that the ingredient lists provided contain no cycles (meaning there are no compound items whose ingredients contain itself.)<br /> 


<h2>Languages and Environments Used</h2>

- <b>Python</b> 
- <b>VS code</b>

<h2>Program walk-through</h2>

<p align="left">
TRANSFORMING recipes:<br/>
Each recipe list can contain both compound and atomic food items. Additionally, each compound food item can have one or more different ingredient lists associated with it. In this structure, if we wanted to look up all the different ways to make a specific compound food item, we'd have to loop over the whole list. Let's consider what questions we might want to ask about our data:<br/>
- Given the name of a food item, can we quickly determine whether it is atomic or compound?<br/>
- Given an atomic food item, can we efficiently determine its cost, helping to determine the total price of a recipe? <br/>
- Given a compound food item, what are all the different ingredient lists we can use to make this item?<br/>

Therefore, a dictionary is a good data structure to use.<br/>

The first function, 'make_recipe_book' takes in a list of recipes, as described in the previous section, and returns a dictionary that maps compound food item names to a list of associated ingredient lists.<br/>
 compound_recipe = {}

        for compound in recipes:
            if compound[0] == "compound":
                if compound[1] not in compound_recipe:
                    compound_recipe[compound[1]] = [compound[2]]
                else:
                    compound_recipe[compound[1]].append(compound[2])
    
        return compound_recipe
<br/>
    
The next function 'make_atomic_costs' also takes in a list of recipes and returns a dictionary of atomic food item names mapped to their cost.<br/>
atomic_recipe = {}

        for atomic in recipes:
            if atomic[0] == "atomic":
                atomic_recipe[atomic[1]] = atomic[2]
    
        return atomic_recipe
<br/>
<p align="left">
Finding the LOWEST cost:<br/>
In this section, we'll write a function that tells us how much the cheapest way to make a particular food item costs, by purchasing all necessary atomic items. We will assume that the database is complete, i.e., that every recipe in the database can be created using some combination of the atomic food items in the database. Calculating the total cost of an ingredient list requires summing the result of multiplying each ingredient's quantity by its calculated cost. For this and later parts of this lab, we'll assume that all quantities of an ingredient come from the same recipe. For example, consider the following recipe list:<br/>
cookie_recipes = [<br/>
    ('compound', 'cookie sandwich', [('cookie', 2), ('ice cream scoop', 3)]),<br/>
    ('compound', 'cookie', [('chocolate chips', 3)]),<br/>
    ('compound', 'cookie', [('sugar', 10)]),<br/>
    ('atomic', 'chocolate chips', 200),<br/>
    ('atomic', 'sugar', 5),<br/>
    ('compound', 'ice cream scoop', [('vanilla ice cream', 1)]),<br/>
    ('compound', 'ice cream scoop', [('chocolate ice cream', 1)]),<br/>
    ('atomic', 'vanilla ice cream', 20),<br/>
    ('atomic', 'chocolate ice cream', 30),<br/>
]<br/>

As written, a cookie sandwich must contain two of the same cookies and three of the same ice cream scoops. So in this case there are four possible ways we could make a cookie sandwich:<br/>
- 6 chocolate chips (cost = 200 each) & 3 vanilla ice cream (cost = 20 each)<br/>
- 6 chocolate chips  (cost = 200 each) & 3 chocolate ice cream (cost = 30 each)<br/>
- 20 sugar (cost = 5 each) & 3 vanilla ice cream (cost = 20 each)<br/>
- 20 sugar (cost = 5 each) and 3 chocolate ice cream (cost = 30 each)<br/>

Note that we aren't considering possibilities that fulfil the 3-ice-cream-scoop requirement by having 2 chocolate ice cream and 1 vanilla ice cream, or any other combination. If we wanted to allow for mixing and matching ice cream scoops within the cookie sandwich recipe, we could have included the following ingredient list instead:<br/>
('compound', 'cookie sandwich', [('cookie', 1), ('cookie', 1), ('ice cream scoop', 1), ('ice cream scoop', 1), ('ice cream scoop', 1)])<br/>

Also, we will consider two types of items to help think of potential failure modes of our approach so far:<br/>
1. Nonexistent Items: if the database came from a local grocery store, you can imagine that it might run out of stock of particular items sometimes. Since we can't make a recipe if one (or more) of the ingredients is missing, we should take this scenario into account. Ensure that 'lowest_cost' returns None if it is given the name of a food item that is not present in the database. Additionally, consider any recipe that includes a missing food item to be impossible to complete. For example, let's consider our dairy_recipes database again:<br/>
dairy_recipes = [<br/>
    ('compound', 'milk', [('cow', 2), ('milking stool', 1)]),<br/>
    ('compound', 'cheese', [('milk', 1), ('time', 1)]),<br/>
    ('compound', 'cheese', [('cutting-edge laboratory', 11)]),<br/>
    ('atomic', 'milking stool', 5),<br/>
    ('atomic', 'cutting-edge laboratory', 1000),<br/>
    ('atomic', 'time', 10000),<br/>
    ('atomic', 'cow', 100),<br/>
]<br/>

Now let's imagine that the entry for 'cow' was no longer present:<br/>
dairy_recipes_2 = [<br/>
    ('compound', 'milk', [('cow', 2), ('milking stool', 1)]),<br/>
    ('compound', 'cheese', [('milk', 1), ('time', 1)]),<br/>
    ('compound', 'cheese', [('cutting-edge laboratory', 11)]),<br/>
    ('atomic', 'milking stool', 5),<br/>
    ('atomic', 'cutting-edge laboratory', 1000),<br/>
    ('atomic', 'time', 10000),<br/>
]<br/>

In this case, calling lowest_cost(dairy_recipes_2, 'cow') returns None. Calling lowest_cost(dairy_recipes_2, 'milk') also returns None because in this case 'milk' cannot be made without 'cow'. If we went further and also removed 'cutting-edge laboratory', then lowest_cost would return None if we tried to calculate the cost of 'cheese', since there is no way to make it using the remaining atomic items.

2) Forbidden Items: sometimes when preparing food, we want to avoid using certain ingredients, even if they are technically available. For example, consider making food for someone with a dietary restriction; they may ask you not to include a particular food item even if it is available from the store. Ensure that there is an optional parameter to the lowest_cost function, so that we can optionally provide an iterable of food item names to ignore. Now, calling lowest_cost(dairy_recipes_2, 'cheese', ["cutting-edge laboratory"]) provides the same results as if we removed 'cutting-edge laboratory' from the database, but lowest_cost(dairy_recipes_2, 'cheese') works as before.<br/>
<br/>
<br/>

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
<br/>
<p align="left">
Finding the CHEAPEST FLAT recipe:<br/>
Now, we can figure out how much money to take to the grocery store, taking into account their stock and things like dietary restrictions or foods that you or your friends don't like. But this only tells us how much money we need to take to the store; it doesn't actually tell us what to buy. <br/>

Unlike 'lowest_cost', given  a recipes list and the name of a food item, this function returns a "flat recipe", representing the cheapest full recipe for the given food item. "flat recipe" is a dictionary mapping the necessary atomic food items to their quantities. Importantly, a flat recipe dictionary only contain atomic food items, and it contains the right number to build the original food item completely (possibly by creating other intermediate food items along the way).If the same minimal cost could be achieved by multiple different recipes, it returns any of those recipes.<br/>

For example, let's return to our dairy_recipes example from earlier. Calling cheapest_flat_recipe(dairy_recipes, 'cheese') returns:<br/>

{'cow': 2, 'milking stool': 1, 'time': 1}<br/>

Calling cheapest_flat_recipe(dairy_recipes, 'cheese', ['cow']) returns:<br/>
{'cutting-edge laboratory': 11}<br/>

The code is as follows:<br/>

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
<br/>
HELPER FUNCTIONS:<br/>
1. scale_recipe: takes a flat_recipe dictionary and returns a new flat_recipe with all values scaled by n, wihtout mutating the input.<br/>

        scaled_flat_recipe = {}
    
        for item in flat_recipe:
            scaled_flat_recipe[item] = flat_recipe[item] * n
    
        return scaled_flat_recipe
<br/>
2. make_grocery_list: takes a list of flat_recipes and returns a new flat_recipe dictionary which includes all the keys mapped to the sum of the corresponding values across all the dictionaries, without mutating the input. For example, make_grocery_list([{'milk':1, 'chocolate':1}, {'sugar':1, 'milk':2}]) returns {'milk':3, 'chocolate': 1, 'sugar': 1}. <br/>

       grocery_list = {}
   
       for flat in flat_recipes:
           for item in flat:
               if item not in grocery_list:
                   grocery_list[item] = flat[item]
               else:
                   grocery_list[item] += flat[item]
   
       return grocery_list

<br/>
3. flat_recipe_cost: returns cost of items in flat_recipe.

       sum_cost = []
       for item in flat_recipe:
           cost = flat_recipe[item] * make_atomic_costs(recipes)[item]
           sum_cost.append(cost)
   
       return sum(sum_cost)
<br/>
<p align="left">
All FLAT recipes:<br/>
In some cases, we may want to consider other ways of creating that food item as well. In this final section, I have written some functions that can help us find all of the ways we could create a given food item. This function produces a list of dictionaries representing each possible flat recipe that can be constructed from the given recipe list. The list returned may contain the appropriate elements in any order and duplicates.<br/>
 
For example, there are several different ways to make a 'burger', depending on which way we choose to make the burger, how we make the cheese, and whether we choose the fancy ketchup:<br/>
-{'yeast': 2, 'salt': 2, 'flour': 4, 'cutting-edge laboratory': 22, 'lettuce': 1, 'cow': 2}:<br/>
-{'yeast': 2, 'salt': 2, 'flour': 4, 'cow': 4, 'milking stool': 2, 'time': 2, 'lettuce': 1}:<br/>
-{'yeast': 2, 'salt': 2, 'flour': 4, 'cutting-edge laboratory': 11, 'lettuce': 1, 'cow': 1, 'tomato': 30, 'vinegar': 5}:<br/>
-{'yeast': 2, 'salt': 3, 'flour': 4, 'cutting-edge laboratory': 11, 'lettuce': 1, 'cow': 1, 'tomato': 30, 'vinegar': 3, 'sugar': 2, 'cinnamon': 1}:<br/>
-{'yeast': 2, 'salt': 2, 'flour': 4, 'cow': 2, 'milking stool': 1, 'time': 1, 'lettuce': 1, 'tomato': 30, 'vinegar': 5}:<br/>
-{'yeast': 2, 'salt': 3, 'flour': 4, 'cow': 2, 'milking stool': 1, 'time': 1, 'lettuce': 1, 'tomato': 30, 'vinegar': 3, 'sugar': 2, 'cinnamon': 1}:<br/>

Without 'milk', we end up with a smaller list of possibilities::<br/>
-{'yeast': 2, 'salt': 3, 'flour': 4, 'cutting-edge laboratory': 11, 'lettuce': 1, 'cow': 1, 'tomato': 30, 'vinegar': 3, 'sugar': 2, 'cinnamon': 1}:<br/>
-{'yeast': 2, 'salt': 2, 'flour': 4, 'cutting-edge laboratory': 11, 'lettuce': 1, 'cow': 1, 'tomato': 30, 'vinegar': 5}:<br/>
-{'yeast': 2, 'salt': 2, 'flour': 4, 'cutting-edge laboratory': 22, 'lettuce': 1, 'cow': 2}:<br/>





