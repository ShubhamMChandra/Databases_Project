# Databases_Project

## Arushi Update - 12/06

Check out the 'Cleaned Data' directory.

- `recipes.csv` - Data for around 1k recipes which includes a bunch of fields. We can ignore the ones we don't need later. The ones I think are useful are:
  - `id`
  - `name`
  - `description`
  - `servings`
  - `steps`
  - `dishid`
  Note that the `dishid` has been assigned by using an LLM.

- `ingredients.csv` - Contains the fields:
  - `ingredientid`
  - `ingredient_name`
  
  I am working on adding the category and calories.

- `requires.csv` - Captures the relationship between recipes and ingredients. Currently has fields:
  - `recipeid`
  - `ingredientid`
  - `details`
  
  For example: `[1, 7, "1 medium red bell pepper, chopped coarse"]`

- `dishes.csv` - Contains the fields:
  - `dishid`
  - `dishname`
  
  Data generated from running recipe names through an LLM. We don't have cuisine or type in it yet.

- `chefs.csv` - Contains the fields:
  - `Username`
  - `Age`
  - `Id`
  - `Location`
  
  Data for 95 users. For example: `[AvaGlow_09, 54, 94, New York]`

- `friends.csv` - Has fields:
  - `chef1`
  - `chef2`
  - `since`

- `reviews.csv` - Has fields:
  - `chef_id`
  - `recipe_id`
  - `rating`
  - `date`
  
  Rating is between 1 to 5.

- We havent included `Cookbooks` yet, but that should be pretty straightforward. I will get to it tmrw.