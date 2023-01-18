The following repository is my final project for Harvard's Fall 2022 CS50 course. It uses Flask's built in web server and code.cs50.io, which can be accessed by logging into a github account on code.cs50.io.

HOW TO OPEN PROJECT:
- Download project.zip from this repository onto your computer
- Log into code.cs50.io with your github account
- Click on your terminal window, and execute "cd" by itself.
- Execute "mkdir project" to create a directory called project
- Right click within your codespace to upload project.zip
- Execute "unzip project.zip -d project" in your terminal to unzip the project files into the project directory
- Now type "cd project" followed by Enter to move yourself into (i.e., open) that directory.
- Before getting started, we’ll need to register for an API key. For simplicity, you can use the following: pk_2f61075e186f414f9dc26de683184739
- In your terminal window, execute: $ export API_KEY=pk_2f61075e186f414f9dc26de683184739
- Start Flask’s built-in web server (within project/): by executing "$ flask run"
- Copy paste the link returned in your terminal into a new tab. This should display Songbook!

BACKGROUND AND NAVIGATION
- Songbook is a social media website where people can rate, share, and post about music.
- Upon opening the website, you'll be welcomed by 2 pages: register and login. If you already have an account, log in directly. If not, register with a username, password, and profile picture! Usernames must be unique.
- Once signed in, you can create your own posts via the "post" link in the navbar. Each post must indicate the artist, title, and rating (out of 5), along with a caption
- Once you've signed in, you'll automatically be brought to an explore page, displaying every single post a user has made on the website from most to least recent. You can always return to the navigation page via the explore link on the navbar
- You can also view the website's song leaderboard via the navbar, which will rank every single song in order of descending rank. Rank is determined by aggregating all rankings for that song in the website's database.
- The profile tab in the navigation bar allows you to see your own posts, along with the total number of posts you have made

VIDEO WALKTHROUGH
- Youtube link: https://youtu.be/xDMEpjtisUw
