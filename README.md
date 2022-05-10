# Stack Overflow in Russian Comment Moderator

This is a auto moderator that helps us to track rude comments on Stack Overflow in Russian

# Take A Look At It Live

The app is live with the besic model ever: https://chat.stackexchange.com/rooms/73258/. Admin app is depoyed on http://benice.rudevs.ru/

# Specification Or How It Words

The app is structured in the following way.

1. We create a database and upload initial data.
2. The initial data contains ~6K of comments (1.5K rude comments and the rest is normal ones).
3. We build a logistic regression model and store it in the database.
5. Each 10 minutes the app pulls new comments from Stack Exchange servers via public API and stores it locally in the database.
7. Each 10 minutes the app analyses comments in the database with the logistic regression model and marks comments as rude if necessary.
8. If a comment is marked as rude it will appear in an RSS feed `http://benice.rudevs.ru/comments/feed/`. 
9. The feed is added to a [chat room](https://chat.stackexchange.com/rooms/73258/). Anyone can monitor this chat and see if something wrong happens on our site.

I've built an additional “admin” module where we can 

1. See how the features are distributed among all analysed comments.
2. See ROC for all models.
3. Verify comments that were marked as rude. When there are more than 50 verified comments the model gets retrained and starts reanalysing all comments in the database.

## Screenshots

### The chat room

![](https://i.stack.imgur.com/LT4ig.jpg)

### Feature distribution

![](https://i.stack.imgur.com/1ywqW.png)

### ROC

![](https://i.stack.imgur.com/dbPAB.png)

### Verifying comments

![](https://i.stack.imgur.com/UN5Ew.png)
