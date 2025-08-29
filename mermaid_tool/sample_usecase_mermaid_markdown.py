SAMPLE_ER_DIAGRAM = """
erDiagram
    CUSTOMERS ||--o{ ORDERS : has
    ORDERS ||--o{ ORDER_DETAILS : contains
    ORDER_DETAILS }o--|| PRODUCTS : references
    CUSTOMERS {
        int CustomerID PK
        string FirstName
        string LastName
    }
    ORDERS {
        int OrderID PK
        int CustomerID FK
        date OrderDate
    }
    ORDER_DETAILS {
        int OrderID FK,PK
        int ProductID FK,PK
        int Quantity
    }
    PRODUCTS {
        int ProductID PK
        string ProductName
    }
"""

DB_SCHEMA = """
    graph TD
        subgraph Customers
            C1[CustomerID: INT PK]
            C2[FirstName: VARCHAR]
            C3[LastName: VARCHAR]
        end
        subgraph Orders
            O1[OrderID: INT PK]
            O2[CustomerID: INT FK]
            O3[OrderDate: DATE]
        end
        subgraph OrderDetails
            OD1[OrderID: INT FK, PK]
            OD2[ProductID: INT FK, PK]
            OD3[Quantity: INT]
        end
        subgraph Products
            P1[ProductID: INT PK]
            P2[ProductName: VARCHAR]
        end
        Customers --> Orders
        Orders --> OrderDetails
        OrderDetails --> Products
"""

JOIN_DIAGRAM = """
graph LR
    A[Customers] -->|"INNER JOIN<br>on c.CustomerID = o.CustomerID"| B[Orders]
    B -->|"LEFT JOIN<br>on o.OrderID = od.OrderID"| C[OrderDetails]
    C -->|"RIGHT JOIN<br>on od.ProductID = p.ProductID"| D[Products]
    subgraph Filters
        F1[WHERE o.OrderDate >= '2023-01-01']
        F2[ORDER BY o.OrderID]
    end

"""