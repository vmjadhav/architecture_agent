SEQUENCE_DIAGRAM = """
sequenceDiagram
    participant User
    participant WebApp
    participant AuthService
    participant UserDB
    participant NotificationService
    participant OrderService
    participant InventoryAPI
    participant PaymentGateway
    participant AdminDashboard

    User->>WebApp: Register
    WebApp->>AuthService: CreateUser(username, password)
    AuthService->>UserDB: INSERT new user
    UserDB-->>AuthService: Success or error
    alt Registration successful
        AuthService-->>WebApp: Success
        WebApp->>NotificationService: Send Welcome Email
        NotificationService-->>User: Welcome Email
        User->>WebApp: Login
        WebApp->>AuthService: Authenticate(username, password)
        AuthService-->>WebApp: JWT token
        WebApp->>OrderService: Place Order (token)
        OrderService->>UserDB: Get User Info
        UserDB-->>OrderService: User Info
        OrderService->>InventoryAPI: Reserve Items
        InventoryAPI-->>OrderService: Reservation Success/Fail
        alt Inventory reserved
            OrderService->>PaymentGateway: Create Payment Intent
            PaymentGateway-->>OrderService: Payment Success/Fail
            alt Payment Success
                OrderService-->>User: Order Confirmation
                OrderService->>NotificationService: Order Placed Email
                NotificationService-->>User: Order Email
                OrderService->>AdminDashboard: Update Order Status
            else Payment Fail
                OrderService-->>User: Payment Error Message
            end
        else Inventory fail
            OrderService-->>User: Out of Stock Message
        end
    else Registration error
        AuthService-->>WebApp: Error
        WebApp-->>User: Error message
    end

"""


ER_DIAGRAM = """
erDiagram
    CUSTOMER {
        int id PK
        string name
        string email
        string address
    }
    ORDER {
        int id PK
        date order_date
        int customer_id FK
    }
    PRODUCT {
        int id PK
        string name
        float price
    }
    ORDER_ITEM {
        int id PK
        int order_id FK
        int product_id FK
        int quantity
        float unit_price
    }

    CUSTOMER ||--o{ ORDER : places
    ORDER ||--o{ ORDER_ITEM : contains
    PRODUCT ||--o{ ORDER_ITEM : includes
    """

FLOW_CHART = """
flowchart TD
    subgraph User Access Layer
        U1(User Web Browser)
        U2(Mobile App)
    end

    subgraph Frontend Apps
        FE1[React Web App]
        FE2[Flutter Mobile App]
    end

    subgraph API Gateway & Authentication
        AGW(API Gateway)
        OAUTH(OAuth2 Service)
        SSO(SSO/IDaaS)
    end

    subgraph Backend Services
        B1(User Service)
        B2(Order Service)
        B3(Product Service)
        B4(Analytics Service)
        B5[Async Worker/Consumer]
    end

    subgraph Messaging & Events
        MQ1[Kafka Topic: OrderEvents]
        MQ2[Kafka Topic: UserEvents]
    end

    subgraph Data Storage
        DB1[(PostgreSQL - UserDB)]
        DB2[(MongoDB - Orders)]
        DB3[(Redis - Session Cache)]
        DW[(BigQuery Data Lake)]
    end

    subgraph External Integrations
        EXT1[(Payment Gateway Stripe)]
        EXT2[Shipping API]
        EXT3[(S3 Bucket Data Export)]
    end

    subgraph Monitoring & Ops
        LOG[(Centralized Logging ELK)]
        METRICS[(Metrics & Dashboard Prometheus, Grafana)]
        ALERT[(Alerting Slack/Email)]
    end

    %% User Interaction
    U1 --> FE1
    U2 --> FE2
    FE1 --> AGW
    FE2 --> AGW
    AGW --> OAUTH
    OAUTH --> SSO
    AGW --> B1
    AGW --> B2
    AGW --> B3
    AGW --> B4

    %% Internal Service Calls
    B1 -- read/write --> DB1
    B1 -- user events --> MQ2
    B2 -- order events --> MQ1
    B2 -- read/write --> DB2
    B3 -- read --> DB2
    B4 -- analytics ETL --> DW
    B5 -- async tasks --> DB2

    %% Event-Driven Interactions
    MQ1 -- consumed by --> B5
    MQ2 -- consumed by --> B5

    %% External Integrations
    B2 -- payment --> EXT1
    B2 -- shipping --> EXT2
    B4 -- export data --> EXT3

    %% Cache and Performance
    FE1 -- session --> DB3
    FE2 -- session --> DB3
    B1 -- cache read/write --> DB3

    %% Monitoring & Ops
    B1 --> LOG
    B2 --> LOG
    B3 --> LOG
    B5 --> LOG
    AGW --> LOG
    LOG --> ALERT
    B1 --> METRICS
    B2 --> METRICS
    B3 --> METRICS
    AGW --> METRICS
    METRICS --> ALERT
"""

ARCHITECTURE_DIAGRAM = """
flowchart TD
    %% API Group
    lb[Load Balancer]
    auth[Auth Service]
    server[Server]
    db[Database]

    %% Storage Group
    disk1[Storage 1]
    disk2[Storage 2]
    cache[Cache]

    %% Analytics Group
    analytics[Analytics Service]

    %% Monitoring Group
    monitoring[Monitoring]

    %% Connections
    lb --> auth
    auth --> server
    server --> analytics
    server --> monitoring
    cache --> server
    server --> db
    db --> disk2
    disk1 --> server
    disk2 --> db

    %% Optional: Grouping using subgraphs for visual separation
    subgraph API
        lb
        auth
        server
        db
    end

    subgraph Storage
        disk1
        disk2
        cache
    end

    subgraph Analytics
        analytics
    end

    subgraph Monitoring
        monitoring
    end
"""

CLASS_DIAGRAM = """
classDiagram
    Animal <|-- Duck
    Animal <|-- Fish
    Animal <|-- Zebra
    Animal : +int age
    Animal : +String gender
    Animal: +isMammal()
    Animal: +mate()
    class Duck{
      +String beakColor
      +swim()
      +quack()
    }
    class Fish{
      -int sizeInFeet
      -canEat()
    }
    class Zebra{
      +bool is_wild
      +run()
    }
"""

XY_BAR_DIAGRAM = """
xychart-beta
    title "Sales Revenue"
    x-axis [jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec]
    y-axis "Revenue (in $)" 4000 --> 11000
    bar [5000, 6000, 7500, 8200, 9500, 10500, 11000, 10200, 9200, 8500, 7000, 6000]
    line [5000, 6000, 7500, 8200, 9500, 10500, 11000, 10200, 9200, 8500, 7000, 6000]
"""

PIE_CHART = """
pie title Payment Methods Usage
    "Credit Card" : 45
    "Debit Card" : 25
    "UPI" : 20
    "Wallet" : 10
"""

KANBAN_BOARD = """
%%{init: { 'kanban': { 'ticketBaseUrl': 'https://github.com/mermaid-js/mermaid/issues/#TICKET#' }}}%%
kanban
  Todo
    [Create Documentation]
    docs[Create Blog about the new diagram]
  [In progress]
    id6[Create renderer so that it works in all cases. We also add some extra text here for testing purposes. And some more just for the extra flare.]
  id9[Ready for deploy]
    id8[Design grammar]@{ assigned: 'knsv' }
  id10[Ready for test]
    id4[Create parsing tests]@{ ticket: 2038, assigned: 'K.Sveidqvist', priority: 'High' }
    id66[last item]@{ priority: 'Very Low', assigned: 'knsv' }
  id11[Done]
    id5[define getData]
    id2[Title of diagram is more than 100 chars when user duplicates diagram with 100 char]@{ ticket: 2036, priority: 'Very High'}
    id3[Update DB function]@{ ticket: 2037, assigned: knsv, priority: 'High' }
  id12[Can't reproduce]
    id3[Weird flickering in Firefox]
"""