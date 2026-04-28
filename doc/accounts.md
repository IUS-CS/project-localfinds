# LocalFinds - Accounts

This module provides database operations for user account management
using SQLite.

It supports:

- Account creation
- Retrieval by ID or username
- Updating account details
- Deletion of accounts
- Reset of accounts table

Each function manages its own database connection and ensures
proper cleanup after execution.

## Database initialization

**initialize_accounts(accounts)**

Create the accounts table if it does not already exist.

**Table Schema:**

```
id       - Primary key (auto-increment)
username - Unique username (required)
password - Hashed password (required)
bio      - Optional user biography
joined   - Timestamp of account creation
```

**Usage:**
`initialize_accounts("data/accounts.db")`

## Create account

**store_account(accounts, username, password)**

Insert a new user account into the database.

**Args:**

```
accounts (str): Path to SQLite database
username (str): Unique username
password (str): Hashed password
```

**Returns:**

```
True if account was created successfully,
False if username already exists
```

**Usage:**
`store_account("data/accounts.db", "john", hashed_password)`

**Notes:**

- Raises no exception on duplicate usernames
- Password should already be hashed before calling

## Get account by ID

**get_account(accounts, account_id)**

Retrieve a single account by its ID.

**Args:**

```
accounts (str): Database path
account_id (int): User ID
```

**Returns:**

```
dict | None: Account data or None if not found
```

**Usage:**
`get_account_by_username("data/accounts.db", id)`

## Get account by username

**get_account_by_username(accounts, username)**

Retrieve an account using its username.

**Args:**

```
accounts (str): Database path
username (str): Username to search for
```

**Returns:**

```
dict | None: Account data or None if not found
```

**Usage:**
`get_account_by_username("data/accounts.db", "john")`

## Get all accounts

**get_all_accounts(accounts)**
Retrieve all accounts from the database.

**Returns:**

```
list[dict]: List of all user accounts ordered by join date
```

**Usage:**
`get_all_accounts("data/accounts.db")`

## Update account

**update_account(accounts, account_id, username, password, bio="")**

Update an existing user account.

**Args:**

```
accounts (str): Database path
account_id (int): ID of account to update
username (str): New username
password (str): New hashed password
bio (str, optional): Updated biography
```

**Usage:**
`update_account("data/accounts.db", id, "john", new_password, bio="Hello!")`

**Notes:**

- Overwrites all fields provided
- Does not validate uniqueness of username

## Delete account

**delete_account(accounts, account_id)**

Delete a user account by ID.

**Args:**

```
accounts (str): Database path
account_id (int): ID of account to delete
```

**Usage:**
`delete_account("data/accounts.db", id)`

## Clear accounts table

**clear_accounts(accounts)**

Delete all records from the accounts table.

**Warning:**
This is destructive and intended only for testing or demo resets.
