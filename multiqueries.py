import sqlite3

conn = sqlite3.connect('backend.db')
c = conn.cursor()

c.execute('''CREATE TABLE Customers
             (CustomerID INTEGER PRIMARY KEY, FirstName TEXT, LastName TEXT, Email TEXT, DateOfBirth TEXT)''')

c.execute('''CREATE TABLE Products
             (ProductID INTEGER PRIMARY KEY, ProductName TEXT, Price REAL)''')

c.execute('''CREATE TABLE Orders
             (OrderID INTEGER PRIMARY KEY, CustomerID INTEGER, OrderDate TEXT)''')

c.execute('''CREATE TABLE OrderItems
             (OrderItemID INTEGER PRIMARY KEY, OrderID INTEGER, ProductID INTEGER, Quantity INTEGER)''')


c.execute("INSERT INTO Customers VALUES (1, 'John', 'Doe', 'john.doe@example.com', '1985-01-15')")
c.execute("INSERT INTO Customers VALUES (2, 'Jane', 'Smith', 'jane.smith@example.com', '1990-06-20')")

c.execute("INSERT INTO Products VALUES (1, 'Laptop', 1000)")
c.execute("INSERT INTO Products VALUES (2, 'Smartphone', 600)")
c.execute("INSERT INTO Products VALUES (3, 'Headphones', 100)")

c.execute("INSERT INTO Orders VALUES (1, 1, '2023-01-10')")
c.execute("INSERT INTO Orders VALUES (2, 2, '2023-01-12')")

c.execute("INSERT INTO OrderItems VALUES (1, 1, 1, 1)")
c.execute("INSERT INTO OrderItems VALUES (2, 1, 3, 2)")
c.execute("INSERT INTO OrderItems VALUES (3, 2, 2, 1)")
c.execute("INSERT INTO OrderItems VALUES (4, 2, 3, 1)")

conn.commit()

#queries

c.execute("SELECT * FROM Customers")
print("1. All Customers:")
for row in c.fetchall():
    print(row)
print()

c.execute("SELECT * FROM Orders WHERE OrderDate BETWEEN '2023-01-01' AND '2023-01-31'")
print("2. Orders placed in January 2023:")
for row in c.fetchall():
    print(row)
print()

c.execute("""
SELECT Orders.OrderID, Customers.FirstName, Customers.LastName, Customers.Email, Orders.OrderDate
FROM Orders
JOIN Customers ON Orders.CustomerID = Customers.CustomerID
""")
print("3. Order details with customer information:")
for row in c.fetchall():
    print(row)
print()

c.execute("""
SELECT Products.ProductName, OrderItems.Quantity
FROM OrderItems
JOIN Products ON OrderItems.ProductID = Products.ProductID
WHERE OrderItems.OrderID = 1
""")
print("4. Products purchased in Order 1:")
for row in c.fetchall():
    print(row)
print()

c.execute("""
SELECT Customers.CustomerID, Customers.FirstName, Customers.LastName, SUM(Products.Price * OrderItems.Quantity) AS TotalSpent
FROM OrderItems
JOIN Orders ON OrderItems.OrderID = Orders.OrderID
JOIN Customers ON Orders.CustomerID = Customers.CustomerID
JOIN Products ON OrderItems.ProductID = Products.ProductID
GROUP BY Customers.CustomerID
""")
print("5. Total amount spent by each customer:")
for row in c.fetchall():
    print(row)
print()

c.execute("""
SELECT Products.ProductName, SUM(OrderItems.Quantity) AS TotalQuantity
FROM OrderItems
JOIN Products ON OrderItems.ProductID = Products.ProductID
GROUP BY Products.ProductID
ORDER BY TotalQuantity DESC
LIMIT 1
""")
print("6. Most popular product:")
print(c.fetchone())
print()

c.execute("""
SELECT
    strftime('%Y-%m', Orders.OrderDate) AS Month,
    COUNT(Orders.OrderID) AS TotalOrders,
    SUM(Products.Price * OrderItems.Quantity) AS TotalSales
FROM OrderItems
JOIN Orders ON OrderItems.OrderID = Orders.OrderID
JOIN Products ON OrderItems.ProductID = Products.ProductID
WHERE Orders.OrderDate BETWEEN '2023-01-01' AND '2023-12-31'
GROUP BY Month
ORDER BY Month
""")
print("7. Monthly orders and sales in 2023:")
for row in c.fetchall():
    print(row)
print()

c.execute("""
SELECT Customers.CustomerID, Customers.FirstName, Customers.LastName, SUM(Products.Price * OrderItems.Quantity) AS TotalSpent
FROM OrderItems
JOIN Orders ON OrderItems.OrderID = Orders.OrderID
JOIN Customers ON Orders.CustomerID = Customers.CustomerID
JOIN Products ON OrderItems.ProductID = Products.ProductID
GROUP BY Customers.CustomerID
HAVING SUM(Products.Price * OrderItems.Quantity) > 1000
""")
print("8. Customers who spent more than $1000:")
for row in c.fetchall():
    print(row)

conn.close()
