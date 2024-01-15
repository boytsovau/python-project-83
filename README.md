### Hexlet tests and linter status:
[![Actions Status](https://github.com/boytsovau/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/boytsovau/python-project-83/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/c2a8fd88bb6ac8352bc7/maintainability)](https://codeclimate.com/github/boytsovau/python-project-83/maintainability)
[![Actions Status](https://github.com/boytsovau/python-project-83/workflows/page_analyzer-check/badge.svg)](https://github.com/boytsovau/python-project-83/actions)

# Page Analyzer

Page Analyzer is a comprehensive web application built on the Flask framework, embodying modern web development principles based on the MVC architecture. This project covers essential aspects of web development, including routing, request handling, templating, and database interaction.

## Features and Technologies Used

- **MVC Architecture:** The project follows the Model-View-Controller architecture, where Flask acts as the framework handling routing, request handling, and database interaction.
  
- **HTTP Protocol and Client-Server Architecture:** The backbone of web development relies on the HTTP protocol and the client-server architecture. Every interaction with the site involves an HTTP request, and the visible outcome is an HTTP response.

- **Database Design:** Proper database design is crucial for collecting and managing data. The project emphasizes knowledge of normalization forms and relationship principles. SQL queries are executed using the psycopg library.

- **Frontend with Bootstrap:** The frontend is an integral part of web development. Bootstrap, a popular framework, is used for styling and visual presentation, ensuring a seamless integration of backend and frontend components.

- **Infrastructure Elements:** The project encompasses various infrastructure elements, including setting up a web server, installing a database, and understanding basic TCP protocol, IP addresses, and ports.

- **Deployment to Production:** Deployment is an essential part of development, and the project demonstrates an automated deployment approach using the render.com service, which operates as a Platform-as-a-Service (PaaS).

## Getting Started

1. **Clone the Repository:**
   ```bash
   git clone git@github.com:boytsovau/python-project-83.git
   cd page-analyzer
   ```

## Project Deployment:

1. **Install Dependencies:**

    ```bash
    make install
    ```

2. **Run the Application (Development Mode):**

    ```bash
    make dev
    ```

3. **Run the Application (Production Mode):**

    ```bash
    make start
    ```

    By default, the application will be available at `http://localhost:8000`. You can customize the port using the `PORT` variable.

54. **Build the Project:**

    ```bash
    make build
    ```
      This assumes you have a file named `database.sql` with SQL statements for table creation. Ensure the `database.sql` file is present in the repository.

    This command executes the necessary steps to build the project.

Now, your project should be fully deployed and accessible.


## Technologies Used

- **Flask**
- **Bootstrap**
- **psycopg**
- **render.com**



Examlpe project: https://python-project-83-0an4.onrender.com
