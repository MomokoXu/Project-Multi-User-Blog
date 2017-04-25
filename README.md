# Multi User Blog Web Application
![Image of webpage](https://github.com/MomokoXu/Project-Multi-User-Blog/blob/master/project/web-sample.png)
## Introduction
This project aims to implement a multiple user blog web application using Google App Engine. It allows users to sign up for a new account and log in after signing up. It also allows users to search for a particular post by post id and create a new post after logging in. Users can look through the latest posts with or without logging in.

Hope you enjoy this project!

## Main tools and libraries
* Languages: Python, HTML, CSS
* Libraries:
    * [webapp2](https://webapp2.readthedocs.io/en/latest/): from Google App Engine, used for running this application.
    * [db](https://cloud.google.com/appengine/docs/standard/python/refdocs/google.appengine.ext.db): from Google App Engine, used for storing user information and posts data
    * [Jinjia](http://jinja.pocoo.org/): python template engine, used for inline expressions and sandboxed environment.
    * [hashlib](https://docs.python.org/2/library/hashlib.html) and [hmac](https://docs.python.org/2/library/hmac.html): Python built-in library, used for secure cookies and passwords by hashing.

## Features
1. [Front page](https://momokotest-164402.appspot.com/): provides different options for users to choose. If action taken is not appropriate, error message will show up for the corresponding action.
2. [Login](https://momokotest-164402.appspot.com/login): allows returning users to log in. If username does not exist or password is wrong, error message will display.
3. [Signup](https://momokotest-164402.appspot.com/signup): allows the new user to sign up for a new account. If username already exists or passwords not match, error message will display.
4. [Latest posts](https://momokotest-164402.appspot.com/blog): gives a list of the latest posts. Each post has the title of the post, the author of the post, the date created for the post and the content of the post.
5. Find a particular post: allows users to search for a particular post by post id which will be shown on the URL after the user create a new post.
6. [Create a new post](https://momokotest-164402.appspot.com/blog/newpost): allows users who are logged in to create a new post. If the user are not logged in, error message will display. If not both subject and content for the blog are filled, error message will display.
7. [Logout](https://momokotest-164402.appspot.com/logout): allows users to log out from current account.
8. This web app is responsive for different viewports.

## How to use it
* This project has deployed on Google App Engine, so just simple open [this front page](https://momokotest-164402.appspot.com/) in your browser to explore more.

## Source code:
All source codes are in `\project`, please switch to `\project` to explore more.

## Author
[Yingtao Xu](https://github.com/MomokoXu)

## Copyright
This is a project for practicing skills in databses and backend courses not for any business use. Some templates are used from [Udacity FSND program](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004). Please contact me if you think it violates your rights.