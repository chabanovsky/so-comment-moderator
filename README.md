# Stack Overflow in Russian Comment Moderator

This is a auto moderator that helps me to track rude comments on Stack Overflow in Russian

Basically for a long time I had been reviewing most of the posts on Stack Overflow in Russian until we had something like 100 questions per day. Then I started reviewing only questions from new users wich I have not done anymore for a year almost. 

Over that time I found that it's really hard for some people to keep calm when they see something, let's say, not 100% suitable for our site. I mean, badly written questions. The people may sometimes forget that if one writes poor questions that means one and only one thing — this person writes poor questions. It does not mean that the person is a "bad" one. Currently I cannot do so anymore because of the number of comments. On the other hand with more and more new users that visit the site very day the need for moderation increases. I hope this robo–moderator will help us keep kindness atmosphere in the community regardless any obstacles in our way!


# Take A Look At It Live

As it's said: first rule of a ML project is do not use ML in the project! The app is live with the besic model ever https://chat.stackexchange.com/rooms/73258/


# Specification Or How It Words

The app is structured in the following way.

1. We create a database, upload test data to servers.
2. The test data contains ~6K of comments (1.5K rude comments that were flagged as rude or offensive, the rest is normal comments).
3. We build a logistic regression model. Positive class is rude comments. To build the model we use (a) the bag of words (b) plus manually added features. Manual features are different dictionaries created either by me based on vulgar words in the real data or what I found on Internet (mostly on wiktionary.org).
4. We store the model in the database.
5. Each 10 minutes the app sends a query for new comments to Stack Exchange servers view public API. All comments received from SE dumped to the database.
7. Each 10 minutes the app analyses comments in the database with the logistic regression model and marks comments as rude if necessary.
8. If a comment is marked as rude it will appear in a RSS feed `http://benice.rudevs.ru/comments/feed/`. 
9. The feed is added to a [chat room](https://chat.stackexchange.com/rooms/73258/). Anyone can monitor this chat to see if something wrong happens on our site.

I built an additional “admin” module where we can 

1. See how the features are presented in the all analysed comments.
2. See a ROC of the current model.
3. Verify comments that were marked as rude. 

When we verify marked as rude comments we tell our model where it was wrong. If there are more than 50 verified comments the model gets rebuilt automatically and reanalyses the comments in the database.

## Screenshots

### The chat room

![](https://i.stack.imgur.com/LT4ig.jpg)

### Feature distribution

![](https://i.stack.imgur.com/1ywqW.png)

### ROC

![](https://i.stack.imgur.com/dbPAB.png)

### Verifying comments

![](https://i.stack.imgur.com/UN5Ew.png)
