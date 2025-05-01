# CS411-Pokemon-Project

# What the application does at a high level
Applications focus on overarching functionality and purpose of the application. We look at the bigger picture than just the implementations of the modules or components. Developeres that create applications pay attention on how every modules in the system can interact with each other. High level is crucial for system's purpose and effective communication.

# Routes Documentation

### Route: `/api/health`

- **Request Type:** `GET`  
- **Purpose:** Verifies that the service is up and running.

#### Request Body:
_None_

#### Response Format: JSON

**Success Response Example:**
- **Code:** `200`  
- **Content:**
```json
{
  "status": "success",
  "message": "Service is running"
}
```

### Route: `/create-user`

- **Request Type:** `PUT`  
- **Purpose:** Register a new user account.

#### Request Body:
- `username` (String): The desired username.  
- `password` (String): The desired password.

#### Response Format: JSON

**Success Response Example:**
- **Code:** `201`  
- **Content:**
```json
{
  "message": "User 'username123' created successfully",
  "status": "success"
} 
```

**Error Response Example:**
- **Code:** `400`  
- **Content:**
```json
{
  "message": "Username and password are required",
  "status": "error"
} 
```
- **Code:** `400`  
- **Content:**
```json
{
  "message": "error string",
  "status": "error"
} 
```
- **Code:** `500`  
- **Content:**
```json
{
  "message": "An internal error occurred while creating users",
  "status": "error",
  "details": "error string"
} 
```
#### Example Request:
- username: newuser123
- password: securepassword
#### Example Response:
- message: User 'username123' created successfully
- status: 200

### Route: `/login`

- **Request Type:** `POST`  
- **Purpose:** Authenticate a user and log them in

#### Request Body:
- `username` (String): the username of the user.  
- `password` (String): the password of the user.

#### Response Format: JSON

**Success Response Example:**
- **Code:** `200`  
- **Content:**
```json
{
  "message": "User 'newuser123' logged in successfully",
  "status": "success"
} 
```

**Error Response Example:**
- **Code:** `400`  
- **Content:**
```json
{
  "message": "Username and password are required",
  "status": "error"
} 
```
- **Code:** `401`  
- **Content:**
```json
{
  "message": "Invalid username or password",
  "status": "error"
} 
```
- **Code:** `401`  
- **Content:**
```json
{
  "message": "error string",
  "status": "error"
} 
```
- **Code:** `500`  
- **Content:**
```json
{
  "message": "An internal error occurred during login",
  "status": "error"
} 
```
#### Example Request:
- username: newuser123
- password: securepassword
#### Example Response:
- message: User 'newuser123' logged in successfully
- status: 200

### Route: `/logout`

- **Request Type:** `POST`  
- **Purpose:** Log out the current user.

#### Response Format: JSON

**Success Response Example:**
- **Code:** `200`  
- **Content:**
```json
{
  "message": "User logged out successfully",
  "status": "success"
} 
```


### Route: `/change-password`

- **Request Type:** `POST`  
- **Purpose:** Change the password for the current user.

#### Request Body:
- `new_password` (String): The new password to set 

#### Response Format: JSON

**Success Response Example:**
- **Code:** `200`  
- **Content:**
```json
{
  "message": "Password changed successfully",
  "status": "success"
} 
```

**Error Response Example:**
- **Code:** `400`  
- **Content:**
```json
{
  "message": "New password is required",
  "status": "error"
} 
```
- **Code:** `400`  
- **Content:**
```json
{
  "message": "str(e)",
  "status": "error"
} 
```
- **Code:** `500`  
- **Content:**
```json
{
  "message": "An internal error occurred while changing password",
  "status": "error"
} 
```
- **Code:** `500`  
- **Content:**
```json
{
  "message": "An internal error occurred during login",
  "status": "error"
} 
```
#### Example Request:
- new_password: newpassword
#### Example Response:
- message: Password changed successfully
- status: 200

### Route: `/reset-users`

- **Request Type:** `DELETE`  
- **Purpose:** Recreate the users table to delete all users.

#### Response Format: JSON

**Success Response Example:**
- **Code:** `200`  
- **Content:**
```json
{
  "message": "Users table recreated successfully",
  "status": "success"
} 
```

**Error Response Example:**
- **Code:** `500`  
- **Content:**
```json
{
  "message": "An internal error occurred while deleting users",
  "status": "error"
} 
```

### Route: `/fetch-pokemon/<string:name>`

- **Request Type:** `GET`  
- **Purpose:** Fetch Pokémon data from the external PokéAPI, return name, attack, and defense, and save it to the database if not already present.

#### Response Format: JSON

**Success Response Example:**
- **Code:** `200`  
- **Content:**
```json
{
  "pokemon": {"name, attack, defense"},
  "status": "success",
  "source": "local database"
} 
```
- **Code:** `201`  
- **Content:**
```json
{
  "pokemon": {"name, attack, defense"},
  "status": "success",
  "source": "external API and saved to DB"
} 
```

**Error Response Example:**
- **Code:** `404`  
- **Content:**
```json
{
  "message": "Pokemon 'name' not found in PokeAPI",
  "status": "error"
} 
```