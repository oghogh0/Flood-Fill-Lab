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





