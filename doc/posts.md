# LocalFinds - Posts

This module provides database operations for managing user posts using SQLite.

Posts represent location-based content created by users and include metadata such as subject, content, address, tags, and timestamps.

It supports:

- Post creation
- Retrieval of individual or all posts
- Search/filtering posts
- Updating posts and authorship
- Deletion of posts
- Reset of posts table for testing/demo purposes

Each function manages its own database connection and ensures proper cleanup after execution.

## Database Initialization

**initialize_posts(posts)**

Creates the posts table if it does not already exist.

**Table Schema:**

```
id - Primary key (auto-increment)
subject - Post title
content - Post body text
author_id - Username of author
address - Location associated with post
tags - Comma-separated tags
created_at - Timestamp of creation
updated_at - Timestamp of last update
```

**Usage:**
`initialize_posts("data/posts.db")`

## Create Post

**store_post(posts, subject, content, author_id, address, tags=None)**

Inserts a new post into the database.

**Args:**

```
posts (str): Path to SQLite database
subject (str): Post title
content (str): Post body content
author_id (str): Username of post author
address (str): Location string
tags (str | None): Optional comma-separated tags
```

**Usage:**
`store_post("data/posts.db", "Hello World", "This is my first post", "john", "123 Main St", "intro, hello")`

## Get Post by ID

**get_post(posts, post_id)**

Retrieves a single post by its ID.

**Returns:**

```
dict | None: Post data or None if not found
```

**Usage:**
`get_post("data/posts.db", 1)`

## Get All Posts

**get_all_posts(posts)**

Retrieves all posts ordered by most recently updated.

**Returns:**

```
list[dict]: All posts in descending update order
```

**Usage:**
`get_all_posts("data/posts.db")`

## Search / Filter Posts

**filter_posts(posts, searchparams)**

Searches posts by matching a query against multiple fields:

```
subject
content
address
tags
author_id
```

**Args:**

```
searchparams (str): Search keyword
```

**Usage:**
`filter_posts("data/posts.db", "pizza")`

**Behavior:**

- Case-insensitive search
- Partial match using SQL LIKE

## Update Post

**update_post(posts, post_id, subject, content, address, tags=None)**

Updates an existing post and refreshes its updated_at timestamp.

**Args:**

```
posts (str): Database path
post_id (int): ID of post to update
subject (str): New title
content (str): New content
address (str): Updated location
tags (str | None): Updated tags
```

**Usage:**
`update_post("data/posts.db", 1, "New Title", "Updated content", "NYC", "update")`

## Update All Posts by Author

**update_all_posts_author(posts, old_author, new_author)**

Updates all posts when a user changes their username.

**Purpose:**

- Ensures post ownership remains consistent after username changes.

**Usage:**
`update_all_posts_author("data/posts.db", "john", "johnny")`

## Delete Post

**delete_post(posts, post_id)**

Deletes a single post by ID.

**Usage:**
`delete_post("data/posts.db", 1)`

## Delete All Posts by Author

**delete_all_posts_by_author(posts, author_id)**

Removes all posts belonging to a specific user.

**Usage:**
`delete_all_posts_by_author("data/posts.db", "john")`

## Clear Posts Table

**clear_posts(posts)**

Deletes all records from the posts table.

**Warning:**
This is destructive and intended only for testing or demo resets.
