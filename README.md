# SnakeScholars - Educational Python Language Courses Website
![Screenshot 2023-07-29 112649](https://github.com/SSKubatov/SoftUni-Final-Web-Project/assets/107368327/f2430e67-9116-4c3f-a223-a4da1b71bc68)
SnakeScholars is a web application built using Django, designed to provide a platform for offering educational Python language courses. The website aims to create an interactive learning environment for aspiring programmers and enthusiasts who wish to master Python and its applications. By offering a variety of courses, SnakeScholars strives to cater to students of different skill levels, ranging from beginners to advanced Python developers.

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Getting Started](#getting-started)
4. [Installation](#installation)

## Introduction
Python is a versatile and widely-used programming language, making it an excellent choice for educational purposes. SnakeScholars is created with the vision of making Python education accessible, engaging, and rewarding. The platform offers a seamless learning experience by combining informative course content, hands-on exercises, and interactive challenges.

## Features
* Course Management: SnakeScholars provides a user-friendly interface for managing courses, allowing administrators to create, update, and organize course content effectively.

* User Authentication: Students can create accounts, log in, and track their learning progress over time.

* Course Enrollment: Users can enroll in their preferred Python courses and access the learning materials at their convenience.

* Interactive Learning: The website offers interactive exercises and coding challenges to enhance practical understanding.

* Assessment and Feedback: SnakeScholars conducts regular assessments to evaluate students' performance and provide constructive feedback.

## Getting Started
 Before diving into the Python courses offered by SnakeScholars, users need to create an account. Once registered, they can log in to explore the available courses and start their Python learning journey.


## Installation
To run SnakeScholars locally on your machine, follow these steps:

1. Clone this GitHub repository: `git clone https://github.com/SSKubatov/SoftUni-Final-Web-Project.git`

2. Navigate to the project directory: `cd SoftUni-Final-Web-Project`

3. Create a virtual environment: `python -m venv venv`

4. Activate the virtual environment:
    * On Windows: `venv\Scripts\activate`
    * On macOS and Linux: `source venv/bin/activate`
   
5. Install the required dependencies: `pip install -r requirements.txt`

6. Apply the database migrations: `python manage.py migrate`

7. Create a superuser account to manage the website: `python manage.py createsuperuser`

8. Start the development server: `python manage.py runserver`

9. Open your web browser and access the application at: `http://localhost:8000/`
