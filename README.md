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

In this case, calling lowest_cost(dairy_recipes_2, 'cow') should return None. Calling lowest_cost(dairy_recipes_2, 'milk') should also return None because in this case 'milk' cannot be made without 'cow'. If we went further and also removed 'cutting-edge laboratory', then lowest_cost would return None if we tried to calculate the cost of 'cheese', since there is no way to make it using the remaining atomic items.

2) Forbidden Items: sometimes when preparing food, we want to avoid using certain ingredients, even if they are technically available. For example, consider making food for someone with a dietary restriction; they may ask you not to include a particular food item even if it is available from the store. Ensure that there is an optional parameter to the lowest_cost function, so that we can optionally provide an iterable of food item names to ignore. Now, calling lowest_cost(dairy_recipes_2, 'cheese', ["cutting-edge laboratory"]) provides the same results as if we removed 'cutting-edge laboratory' from the database, but lowest_cost(dairy_recipes_2, 'cheese') works as before.

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



