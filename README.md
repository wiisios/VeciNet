# VeciNet

## Description
This project is a system for managing building consortia. It allows administrators, owners, tenants, and real estate agents to manage users, apartments, buildings, and expenses, following modern standards like RFC 9457 for error handling. It is developed in FastAPI, with a layered architecture.

## Features
- User Management:
Registration, login, update, and deletion of users.
- Building Management:
Creation and management of buildings, apartments, and owners.
- Expense Management:
Creation and allocation of shared or individual expenses.
- Security:
Authentication via JWT with differentiated roles (admin, owner, tenant, real estate).
Error handling based on RFC 9457.

## Project Structure
The project follows a layered architecture (controllers, services, repositories), with clear responsibility management and validations:

src/
├── alembic/
├── app/
│   ├── application/
│   ├── config/
│   ├── domain/
│   ├── persistence/
│   │   ├──models/
│   │   └──repositories/
│   ├── presentation/
│   └── security/
├── helpers.py
└── main.py

## Main Components
- Controllers: Handle routes and HTTP responses.
- Services: Contain business logic.
- Repositories: Handle direct interaction with the database.
- Models: Define entities and DTOs.

## **Database Diagram**

Below is the database diagram using Mermaid, representing the main entities and their relationships.

erDiagram
    USER {
        int id PK
        string name
        string last_name
        string email
        string password
        string role
    }
    BUILDING {
        int id PK
        string name
        string street
        string city
        int zip_code
        int flat_amount
    }
    EXPENSE {
        int id PK
        datetime date
        float total_cost
    }
    FLAT {
        int id PK
        string number
        int building_id FK
        int tenant_id FK
    }
    PROPERTY {
        int id PK
        int owner_id FK
        int flat_id FK
    }
    EXPENSEUSER {
        int id PK
        bool is_paid
        int expense_id FK
        int user_id FK
    }
    EXPENSEITEM {
        int id PK
        string reason
        string description
        float cost
        string invoice_img
        int expense_id FK
    }
    USER ||--|| FLAT : is_tenant_of
    USER ||--o| PROPERTY : owns
    USER ||--o| EXPENSEUSER : has_expenses
    EXPENSE ||--o| EXPENSEITEM : contains
    EXPENSE ||--o| EXPENSEUSER : is_associated_with
    FLAT ||--|| PROPERTY : is_property_of
    BUILDING ||--o| FLAT : contains

### Description of the elements:
- **USER**: Represents users in the system, with fields like id, name, last_name, email, password, and role.
- **BUILDING**: Represents buildings, with data referring to its location and the number of apartments.
- **EXPENSE**: Represents expenses associated with buildings assigned to each user.
- **FLAT**: Represents the apartments or units within the buildings.
- **PROPERTY**: An intermediary table representing the relationship of a user as an owner of an apartment.
- **EXPENSEITEM**: Represents each item associated with an expense. It may include an invoice related to that cost.
- **EXPENSEUSER**: An intermediary table representing the relationship between a user and an expense, and whether that expense has been paid or not.

### The diagram shows the relationships between the entities, such as:
- A user can be the owner of multiple apartments.
- A user can be the tenant of only one apartment.
- A user can have many expenses.
- A building has many apartments.
- An expense has many items and is associated with many users.
- An apartment is associated with only one owner.