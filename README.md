# Web Software Development Course Project Plan
## 1. Team
- 604817 Mustafa Kamal
- 62651K Olli Eskola
- 595557 Adisa Adedayo

## 2. Goals
The goal of this project is to build a website where people can buy and play javascript based games and game developer can submit their game. We are aiming to develop all the mandatory and also the optional features listed on the [project description](https://plus.cs.hut.fi/wsd/2016-2017/project/description/). In addition to that, we will also explore the possibility of implementing some more additional features on the way.

## 3. Plans
This section is split in four different subsection. The first one tells about the features that we are going to develop and how we will develop it. The second part explain about the database design of the system. Next, we show some mockups of the application. Lastly, we define the timeline of the project.

### 3.1. Features
list and describe each features and how to develop it
- **Authentication**. The basic login and registration system will be built using Django authentication system. It will also be integrated to the 3rd party login system. We will try to implement login/register using Facebook, Twitter and Github.
- **Browse games**. User will be able to browse games. They can see the recently submitted games, featured games and also popular games. They can also see list of games based on its category. There would also be "similar games" listing on every game page.
- **Buy games**. User can buy games, in order to make the payment to their order, they will have to be authenticated. The payment will be done using the mockup payment service.
- **Play games**. Once the user bought a game, they can play that game. It means that they to login first if they want to play a game.
- **Submit games**. Developers can submit game. They will provide the URL of their self-hosted javascript games along with its description, images and price.
- **Developer dashboard**. One a developer log in to their account. They will have access to the developer dashboard. It contains the listing of all their games where they can edit and/or delete their game. The will also be able to see some sale statistics of their game.
- **Game/service interaction**. The game would be able to communicate with the system using AJAX. They can also utilize the provided API in order to do that.
- **Save and load features**. Player can save their game and load it later in. It will be in the form of JSON data where it will be stored in the database.
- **RESTful API**. We will also implement some simple API for some parts of the game.
- **Javascript game development**. We alos plan to develop our own game. It will most likely a really simple game like tic-tac-toe or rock-paper-scissors kind of game. Apart from that for the other game, we are planning to incorporate some open source javascript games out there and modify the code so that it could comply with our system.  
- **Social media connection**. Along with social media authentication, we will also make sure that the game page itself is shareable with good metadata listing.
- **Ratings and reviews**. This is the additional feature that we will build. User will be able to give ratings and reviews to any game.


### 3.2. Database Schema and Models
This the the entity relationship diagram of the system that we are going to build. The database and Django models will based on this diagram.
![Imgur](http://i.imgur.com/UQg9jCn.png)

Below, you can find additional information about each tables and fields on the diagram above.

#### **user**: contains user data
- **id** [*int(10)*]
- **name** [*string(50)*]
- **email** [*string(50)*]
- **password** [*string(512)*]: will be in SHA encryption
- **pic** [*int(20)*]: foreign key to asset table
- **bio** [*text*]
- **register_date** [*datetime*]
- **last_login** [*datetime*]
- **type** [*string(10)*]: the value can either be "gamer", "developer" or "both"
- **validated** [*boolean*]: used for email validation

#### **game**: contains game data
- **id** [*int(10)*]
- **owner_id** [*int(10)*]: foreign key to user table which will refer to the developer who submit this game
- **title** [*string(100)*]
- **desc** [*text*]
- **instruction** [*text*]
- **url** [*string(512)*]
- **price** [*decimal(6,2)*]

#### **purchase**: contains game purchasing data
- **id** [*int(10)*]
- **buyer_id** [*int(10)*]: foreign key to user table
- **game_id** [*int(10)*]: foreign key to game table
- **date** [*datetime*]
- **amount** [*decimal(6,2)*]

#### **gameplay**: contains data of playing session by the users
- **id** [*int(10)*]
- **player_id** [*int(10)*]: foreign key to user table
- **game_id** [*int(10)*]: foreign key to game table
- **score** [*float*]
- **state** [*varchar(max)*]: in the form of json to store state of the game being played by the user
- **timestamp** [*datetime*]

#### **asset**: contains static assets for users and games such as profile picture, banner, screenshots, video etc
- **id** [*int(10)*]
- **type** [*string(10)*]
- **uri** [*string(512)*]
- **owner_id** [*int(10)*]: foreign key to either user table or game table

#### **taxonomy**: contains categories and tags for game
- **id** [*int(10)*]
- **type** [*string(20)*]
- **label** [*string(50)*]
- **parent_id** [*int(10)*]: foreign key to its own table to determine which is its parent

#### **game_taxonomy**: contain relation between game and its taxonomy (categories and tags)
- **id** [*int(10)*]
- **game_id** [*int(10)*]: foreign key to game table
- **taxonomy_id** [*int(10)*]: foreign key to taxonomy table

#### **review**: contain rate and review from the users
- **id** [*int(10)*]
- **game_id** [*int(10)*]: foreign key to game table
- **reviewer_id** [*int(10)*]: foreign key to user table
- **rating** [*int(1)*]
- **review** [*text*]


### 3.3. Mockups and Views

https://www.dropbox.com/s/275zzn3fv4i56wy/Django-GameStore.pdf?dl=0

## 4. Process and Time Schedule
For communication we will use Slack and for version control Git. We are going to code alone and to meet face-to-face only if needed.

Below is the project timeline. From weeks 52/2016 to 2/2017 we concentrate on mandatory parts and after that we implement the additional features so that the whole project would be ready at the end of week 5/2017. In addition, testing is done continuously every week and that's why it is not included in the timeline.

**Week 52/2016**:
- Database schema creation
- Django framework setup
- Basic authentication system
- Basic UI construction
- Basic developer functionalities (add, remove and modify games)

**Week 1/2017**:
- Basic user functionalities (browse games and search games)
- Basic player functionalities (buy and play games)

**Week 2/2017**:
- Developer dashboard (game inventory and sales statistics, security restrictions)
- Game/service interaction (finishing the game)

**Week 3/2017**:
- Game/service interaction (messages from game to service and vice versa)
- Responsive design polishing
- Social media sharing (Facebook, Twitter, Google)
- 3rd party login (Facebook, Gmail)

**Week 4/2017**:
- Save/load and resolution feature
- RESTful API
- Own game

**Week 5/2017**:
- Own game (cont.)
- Final testing

## 5. Testing and Deployment
Testing will be done using Django unittest, we will develop some test suites for every feature that we develop. On the frontend side, HTML/CSS will be validated in http://validator.w3.org. We will implement simple build system that will lint, compress and combine any CSS and JS files. This build system should also be able to deal with the deployment issue. We will create a branch on our git repository for code which is ready for production where it will finally goes to the production server on Heroku.
