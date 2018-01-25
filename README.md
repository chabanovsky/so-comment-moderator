# Stack Overflow in Russian Comment Moderator

This is a auto moderator that helps me to track rude comments on Stack Overflow in Russian

Basically for a long time I had been reviewing most of the posts on Stack Overflow in Russian until we had something like 100 questions a day. Then I started reviewing only questions from new users wich I have not done do any more for a year almost. 

Over that time I found that it's really hard for some people to keep calm when they see something, let say, not 100% suitable for our site. I mean, badly written questions. The people may sometimes forget that if one writes poor questions that means one and only one thing — this person writes poor questions. It does not mean that the perosn is a "bad" one. So, most of the time I moderated comments on posts but not the posts. I tracked comments and rudness. Currently I cannot do so any more becase of the number of comments and a have planty of stuff to do. On the other hand with more and more new users that visit the site very day the need for moderation increases. I hope this robo–moderator will help us keep kindness atmosphere in the community regardless any obstacles in our way!


# Specification

## Core Features

1. Upload comments via Stack Exchange API once per hour.
2. Put comments into my model.
3. If a comment is rude add it to a database.
4. Based on the database create a RSS-feed of links to rude comments
5. Add this rss-feed to a mod room or to our main chat room.

## Advanced Features

1. Create a web site with a login page for folks who can do something about comments (privileged users and mods)
2. Provide some kind of UI that helps understand if a comment is a rude/spam on a web page and give a way to verify the fact or take an action (invalidate or delete).

## The Model

1. My first model uses cosine similarities as a main argument on judgment of a comment. (Which does not work actually!)
2. The only thing we need is to update the database of rude comments (wich should be uploaded before the initial start).
