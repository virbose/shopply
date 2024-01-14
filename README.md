# shopply
Simple shop and order management API

## Overview

This Django project is a simple online shop where users can view products, make orders, and view their order history. It includes API endpoints for managing products and orders.

## Setup

### Prerequisites

- Python 3.11.x installed
- `pipenv` installed (if not, install it using `pip install pipenv`)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/virbose/shopply.git
   cd shopply
   ```

2. Install dependencies using `pipenv`:

   ```bash
   pipenv install
   ```

3. Activate the virtual environment:

   ```bash
   pipenv shell
   ```

4. Apply database migrations:

   ```bash
   python manage.py migrate
   ```

### Running the Server

To run the development server:

```bash
python manage.py runserver
```

The server will be accessible at `http://localhost:8000/`.

### Database Management

#### Creating Superuser

You can create a superuser to access the Django admin:

```bash
python manage.py createsuperuser
```

Follow the prompts to set a username, email, and password.

##### Creating a token for a user

You can create a DRF token from the command line by running

```bash
python manage.py drf_crete_token <username>
```

#### Setting up the Database

To set up the database and install existing fixtures (for ease of use), you can use the following make command

```bash
make setupdb
```

#### Resetting the Database

If needed, you can reset the database:

```bash
rm db.sqlite3
python manage.py migrate
```
or if using a make command from within `backend`

```bash
make rebuild
```

This will install existing fixtures for customers and products (for ease of use).

### API Endpoints

- Customers: `/api/customers/` - Retrieve information about all customers (as admin), yourself (as regular `Customer`); `AnonymousUser` gets `[]` 
- Products: `/api/products/` - Retrieve information about all products whether logged in or not; `admin`s can create products; paginated endpoint defaulting to 5 items per page; `items_per_page` can change the pagination value.
- Orders: `/api/orders/` - Retrieve information about own orders, as well as create new orders

The assumption is that the `Cart` will be handled in the client logic, at least in this first iteration; this reduces network roundtrips for less relevant information.

### Token Authentication

The API uses Token Authentication as well as BasicAuth. To send authenticated requests:

1. Run the server: `python manage.py runserver`
2. If you go to `http://localhost:8000/api/docs/` you can authorize there and then use the Swagger UI to make requests.
3. Alternatively, in an API client, send a POST request to `http://localhost:8000/api/obtain-token` with your username and password to obtain a token. You can then use this token in the other endpoints by adding the `Authorization: Token <TOKEN>` header to your requests.

### Running Tests

To run tests using `pytest`:

```bash
pipenv run pytest
```

## API Documentation

You can access the interactive  API documentation at 

`http://localhost:8000/api/docs/` - this uses Swagger UI as an interactive tool to play with the API.


## Custom Authentication Model

The project uses a custom authentication model. This is set through `AUTH_USER_MODEL` in `settings.py`.

```python
# settings.py
AUTH_USER_MODEL = 'customers.Customer'
```

## Deployment

### Short-term

To deploy this application to cloud (for the purposes of this excercise, let's say AWS), I would initially go for AWS Elastic Beanstalk. This makes it relatively easy to: 
- Manage the application access
- Configure inbound and outbound traffic
- Set up database configurations (whether replication or multi-AZ db deployment is required)
- Configure load balancing, multi-AZ application deployment and auto-scaling
- Configure logging, monitoring and automated version updates
- Integrate with other AWS Services easily (AWS S3, RDS, Certificate manager etc.)

It is also a relatively low cost solution compared to something like Serverless (AWS Lambda), which, while extremely versatile, is a little bit more costly in terms of infrastructure overhead and traffic cost.

### Mid/long-term

After this initial period, we may want to go for something more comprehensive like AWS CodeCommit + CodeBuild + CodePipeline + CodeDeploy. 
This would be a one-stop-shop solution allowing us to set up a more robust CI/CD pipeline which can handle building application images, pushing those into ECS (or EKS), running entire testing pipelines, as well as pushing successful builds up to production with different strategies. 

### Other considerations

Alternatively, we could choose to handle most of that by using more open source solutions, avoiding being vendor locked into a single provider. Some examples could include using GitLab CI/CD for pipelines and building images upon successful pipeline completion, and ArgoCD or Jenkins for deployment of said services. 

### Non-functional requirements

Some crucial aspects here would be monitoring and alerting: for some low-latency, high-availability services, it is a requirement to ensure that issues are identified and remediated within SLOs to avoid incidents and maintain customer relationships. 

To help with this, code monitoring solutions such as Sentry could be put in place to ensure production errors are captured and reported as soon as possible. At the same time, some realtime alerting services such as OpsGenie might be implemented to flag recurring issues (e.g. an endpoint returning 5xx for 2 minutes) with on-call or in-hours engineers,for a swift resolution.
