# djangoProjectCRUD

 <p>This CRUD application can create posts, publish them in the feed, update and delete. For authentication, 
 JWT is used, for the frontend - Angular, for the backend - Django Rest Framework.</p>

## Running 

Clone the repository:
```
git clone https://github.com/olyaave/djangoProjectCRUD.git
cd djangoProjectCRUD
```

Run the project using the following commands:

Linux:
```
 python manage.py runserver
```
Windows:
```
python manage.py runserver 0:8000
```

## API

### Read 
```
GET /api/posts
```
### Create
```
POST /api/posts
``` 
Only the text of the post is specified in the request body.
```
{
    "body": "Hello world!"
}
```

### Update
```
PUT /api/posts/<int:id>
``` 
The request body specifies the text to replace it with, and the request specifies the id of the post to update.
```
{
    "body": "Hello friend!"
}
```

### Delete

```
DELETE /api/posts/<int:id>
``` 
The request specifies the id of the post to delete.

## Authentication

### Registration

```
POST /registration
```

```
{
    "email": "lupa_and_pupa@gmail.com",
    "username": "Pupa",
    "password": "qwerty1234"
}
```

### Login

```
POST /login
```

```
{
    "email": "lupa_and_pupa@gmail.com",
    "password": "qwerty1234"
}
```

Thank you!
