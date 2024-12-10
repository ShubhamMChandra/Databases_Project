import pandas as pd
import mysql.connector
import sys
from datetime import datetime

# Add your MySQL username and password
USER = 'root'
PASSWORD = ''

# Create connection and cursor object
myConnection = mysql.connector.connect(
    user=USER,
    password=PASSWORD,
    host='localhost',
    database='DataDish'
)
cursorObject = myConnection.cursor()

if myConnection.is_connected():
    print("Connection to MySQL DB successful\n")
else:
    print("Connection to MySQL DB failed\n")
    sys.exit()

# # region Create DB
# try:
#     cursorObject.execute("CREATE DATABASE IF NOT EXISTS DataDish;")
#     myConnection.database = 'DataDish'
#     myConnection.commit()
#     print("Database DatDish created successfully\n")
# except mysql.connector.Error as e:
#     print(f"Error creating database: {e}\n")
#     sys.exit()

# region Create Tables
create_queries = [
    # Dishes
    """
    CREATE TABLE Dishes (
        DishID INT PRIMARY KEY,
        Name VARCHAR(255) NOT NULL,
        Type VARCHAR(255) NOT NULL,
        Cuisine VARCHAR(255)
    );
    """,

    # Cookbooks
    """
    CREATE TABLE Cookbooks (
        CookbookID INT PRIMARY KEY,
        Title VARCHAR(1000) NOT NULL,
        Author VARCHAR(255) NOT NULL,
        PublicationDate DATE NOT NULL
    );
    """,

    # Recipes
    """
    CREATE TABLE Recipes (
        RecipeID INT PRIMARY KEY,
        Title VARCHAR(255) NOT NULL,
        Description TEXT,
        Servings INT,
        Steps TEXT,
        DishID INT NOT NULL,
        CookbookID INT,
        FOREIGN KEY (DishID) 
            REFERENCES Dishes(DishID)
            ON DELETE CASCADE,
        FOREIGN KEY (CookbookID) 
            REFERENCES Cookbooks(CookbookID)
            ON DELETE SET NULL
    );
    """,

    # Ingredients
    """
    CREATE TABLE Ingredients (
        IngredientID INT PRIMARY KEY,
        Name VARCHAR(255) NOT NULL,
        Category VARCHAR(100),
        Calories INT
    );
    """,

    # Requires
    """
    CREATE TABLE Requires (
        RecipeID INT,
        IngredientID INT,
        Details TEXT,
        Quantity INT,
        Unit VARCHAR(50),
        PRIMARY KEY (RecipeID, IngredientID),
        FOREIGN KEY (RecipeID) 
            REFERENCES Recipes(RecipeID)
            ON DELETE CASCADE,
        FOREIGN KEY (IngredientID) 
            REFERENCES Ingredients(IngredientID)
            ON DELETE CASCADE
    );
    """,

    # Chefs
    """
    CREATE TABLE Chefs (
        ChefID INT PRIMARY KEY,
        Username VARCHAR(50) NOT NULL,
        Age INT,
        Location VARCHAR(255)
    );
    """,

    # Reviews
    """
    CREATE TABLE Reviews (
        ChefID INT,
        RecipeID INT,
        Rating INT CHECK (Rating BETWEEN 1 AND 5),
        Date DATE,
        Content TEXT,
        PRIMARY KEY (ChefID, RecipeID),
        FOREIGN KEY (ChefID) 
            REFERENCES Chefs(ChefID)
            ON DELETE CASCADE,
        FOREIGN KEY (RecipeID) 
            REFERENCES Recipes(RecipeID)
            ON DELETE CASCADE
    );
    """,

    # Friends
    """
    CREATE TABLE Friends (
        ChefID1 INT,
        ChefID2 INT,
        FriendsSince DATE,
        PRIMARY KEY (ChefID1, ChefID2),
        FOREIGN KEY (ChefID1) 
            REFERENCES Chefs(ChefID)
            ON DELETE CASCADE,
        FOREIGN KEY (ChefID2) 
            REFERENCES Chefs(ChefID)
            ON DELETE CASCADE
    );
    """
]

try:
    for query in create_queries:
        cursorObject.execute(query)
    print("Tables created successfully\n")
except mysql.connector.Error as e:
    print(f"Error creating tables: {e}\n")
    sys.exit()
myConnection.commit()

# region Load Data
dishes = pd.read_csv('Data/dishes_ct.csv')
cookbooks = pd.read_csv('Data/cookbooks.csv')
recipes = pd.read_csv('Data/recipes.csv')
ingredients = pd.read_csv('Data/ingredients_realistic.csv')
requires = pd.read_csv('Data/requires.csv')
chefs = pd.read_csv('Data/chefs.csv')
reviews = pd.read_csv('Data/reviews_with_content.csv')
friends = pd.read_csv('Data/friends.csv')

# region Insert Data
try:
    # Dishes
    for _, row in dishes.iterrows():
        query = """
        INSERT INTO Dishes (DishID, Name, Type, Cuisine)
        VALUES (%s, %s, %s, %s);
        """
        values = (row['DishID'], row['Name'], row['Type'], row['Cuisine'])
        cursorObject.execute(query, values)
    myConnection.commit()
    print("Dishes insert query executed successfully")

    # Cookbooks
    for _, row in cookbooks.iterrows():
        query = """
        INSERT INTO Cookbooks (CookbookID, Title, Author, PublicationDate)
        VALUES (%s, %s, %s, %s);
        """
        publication_date = datetime.strptime(row['PublicationDate'], '%B %d, %Y').strftime('%Y-%m-%d')
        values = (row['CookbookID'], row['Title'], row['Author'], publication_date)
        cursorObject.execute(query, values)
    myConnection.commit()
    print("Cookbooks insert query executed successfully")

    # Recipes
    for _, row in recipes.iterrows():
        query = f"""
        INSERT INTO Recipes (RecipeID, Title, {'Description,' if not isinstance(row['Description'], float) else ''} Servings, Steps, DishID, CookbookID)
        VALUES (%s, %s, %s, {'%s,' if not isinstance(row['Description'], float) else ''} %s, %s, %s);
        """
        values = (row['RecipeID'], row['Title'])
        values += (row['Description'],) if not isinstance(row['Description'], float) else ()
        values += (row['Servings'], row['Steps'], row['DishID'], row['CookbookID'])
        print(type(row['Description']))
        print("Type:", f'"{(row['Steps'])}"')

        cursorObject.execute(query, values)
    myConnection.commit()
    print("Recipes insert query executed successfully")

    # Ingredients
    for _, row in ingredients.iterrows():
        query = """
        INSERT INTO Ingredients (IngredientID, Name, Category, Calories)
        VALUES (%s, %s, %s, %s);
        """
        values = (row['IngredientID'], row['Name'], row['Category'], row['Calories'])
        cursorObject.execute(query, values)
    myConnection.commit()
    print("Ingredients insert query executed successfully")

    # Requires
    for _, row in requires.iterrows():
        query = f"""
        INSERT INTO Requires (RecipeID, IngredientID {', Details' if not isinstance(row['Details'], float) else ''} {', Quantity' if row['Quantity'] >= 0 else ''} {', Unit' if not isinstance(row['Unit'], float) else ''})
        VALUES (%s, %s{', %s' if not isinstance(row['Details'], float) else ''}{', %s' if row['Quantity'] >= 0 else ''}{', %s' if not isinstance(row['Unit'], float) else ''});
        """
        values = (row['RecipeID'], row['IngredientID'])
        values += (row['Details'],) if not isinstance(row['Details'], float) else ()
        values += (row['Quantity'],) if row['Quantity'] >= 0 else ()
        values += (row['Unit'],) if not isinstance(row['Unit'], float) else ()
        cursorObject.execute(query, values)
    myConnection.commit()
    print("Requires insert query executed successfully")

    # Chefs
    for _, row in chefs.iterrows():
        query = """
        INSERT INTO Chefs (ChefID, Username, Age, Location)
        VALUES (%s, %s, %s, %s);
        """
        values = (row['ChefID'], row['Username'], row['Age'], row['Location'])
        cursorObject.execute(query, values)
    myConnection.commit()
    print("Chefs insert query executed successfully")

    # Reviews
    for _, row in reviews.iterrows():
        query = """
        INSERT INTO Reviews (ChefID, RecipeID, Rating, Date, Content)
        VALUES (%s, %s, %s, %s, %s);
        """
        values = (row['ChefID'], row['RecipeID'], row['Rating'], row['Date'], row['Content'])
        cursorObject.execute(query, values)
    myConnection.commit()
    print("Reviews insert query executed successfully")

    # Friends
    for _, row in friends.iterrows():
        query = """
        INSERT INTO Friends (ChefID1, ChefID2, FriendsSince)
        VALUES (%s, %s, %s);
        """
        values = (row['ChefID1'], row['ChefID2'], row['FriendsSince'])
        cursorObject.execute(query, values)
    myConnection.commit()
    print("Friends insert query executed successfully\n")

except mysql.connector.Error as e:
    print(e)
    print(f"Error inserting data, make sure you have the latest data (version 4) in the Data folder\n")
    sys.exit()

# Close the cursor and the connection
cursorObject.close()
myConnection.close()
