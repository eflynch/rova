# ROVA (internal codename) #
This is a website for fighting misinformation on the internet.

## Installation ##

First install nodejs, python, and postgresql
```
brew install node python postgresql
```

Then install node dependencies
```
cd rova
npm install
npm install -g uglify
npm install -g browserify
```

Then install python dependencies (in a virtualenv)
```
pip install -r requirements.txt
```

Then create a development database
```
createdb rova
```

## Managing Dependencies ##
### Python ###
To install another python package in the virtualenv, use pip
```
pip install packagename
```

Make sure to update the `requirements.txt` file to keep track of what modules are required. `pip freeze` will print out the list of modules currently installed, and `pip freeze > requirements.txt` will write it to the file.

To install all python packages in `requirements.txt`,
```
pip install -r requirements.txt
```

### Node ###
Analogous to pip for python is npm (node package manager) for Node. Javascript was basically invented to run in a browser for scripting HTML. The way that works is you send Javascript files/code along with your HTML to the browser, and then the browser runs the javascript through it's interpreter when it's done loading the page or while it's loading the page. This is very different from code that executes on your server to generate HTML/JS code which then gets sent to the client which are using Python to do. However, you could also do this with Javascript which is what NodeJS is about—-it's a standalone Javascript interpreter that isn't connected to a browser and doesn't have any notion of DOM (document object model) or an HTML page to reference. We are not using Node to actually do any server-side computation, but it is convenient to use Node's package manager to manage client-side dependencies.

Installing a node command for use on the commandline:
```
npm install -g packagename
```

Installing a node module for using in client or server-side code:
```
npm install --save packagename
```

Analogous to `requirements.txt` for pip is `package.json` for npm. The `--save` flag modifies `package.json` to include the newly installed package.

## Database ##
I recommend postgresql for no particular reason over other similar databases. A reason to use a database over something in the file system (besides scalability and enforced consistent schema) is that you have guaruntees when you have concurrent access to it. Access to a database is done on a "transaction" basis, where each transaction can have any number of operations on the records in the database, and you are guarunteed that all of those operations happen together (not interleaved with other transactions that are happening at the same time) (see https://en.wikipedia.org/wiki/ACID).

### Creating / Deleting databases ###
When you start postgres by running the application (should be in /Applications after install), you are starting a local database server which can have many databases in it. 

### Database structure and relationships ###
Each database consists of a set of tables each with a set of columns. A record is a row in one of these tables. Each record in a table has a "primary key" which is basically it's row number and uniquely identifies the record in the table.

A record in one table can reference a record in another table by storing the primary key of the record it is referencing in a column of it's own table. This is then called a "foreign key." That gives you a one-to-one relationship. Other relationships like many-to-one, one-to-many, and many-to-many are also possible.

### Querying database ###
You can query the database directly by running the command
```
psql rova
```
to open a connection to the rova database in the terminal. You can then perform queries as described in the documentation for postgresql as well as a few psql commands that are useful among which are `\q` which is quit, `\d` which is list tables, and `\l` which is list databases.

### Sqlalchemy ###
Most of the time you won't need to write sql queries yourself because there is a python interface called a relational object model. Basically when you create a new model class in python, it gets associated with a table in the database. You can create a new instance of the class and then save it to the database to update the table; you can query an object from the database, modify the python object, and then update it in the database; etc. To see how this works read the documentation for sqlalchemy. The way it is set up now, you will generally want to do something like this to add a new entry to the table.
```
newObject = Object(fields, of, the, object)
db.session.add(newObject)
db.session.commit()
```

### Migrations ###
If you change the schema of your database (by adding/deleting a column, adding/deleting a table, etc.) by changing the code in models.py, these changes aren't immediately reflected in the database. Basically, you need to give the database some commands that tell it how to reshape itself to follow the new schema. Often these are just instructions like, add a new integer column called `myint`, but in some cases you might have very specific instructions for the database if you want to change how you store passwords or something like that which deals with existing data.

The way to deal with these periodic updates to database schema when you perhaps don't want to just delete all the data you have in the database already is called "migrations" and I recommend (and set-up) using a piece of software called `alembic` for handling migrations. Basically, when you change the schema and are ready to migrate the database, you want to run the command
```
python manage.py db migrate
```
which creates a new file in `/migrations/versions` which you can then edit to reflect the changes you made to the database. You can look at the first one as an example and the documentation is fairly good for figuring out how to do simple things like add new tables, etc. In fact, it should autogenerate a fair-amount of the migration but for some reason it doesn't seem to be doing that right now (I'm not sure why). Then, when you are done writing the migration file run
```
python manage.py db upgrade
```
to actually perform the migration and change the database schema. If you don't migrate the database, when you go to make a query in python that doesn't match the existing schema, you will get an error.

## Server ##
The server is set up in the file `__init__.py`. In this file the Flask app is created, the database connection is set-up, the database schema is set, and the routes in `views.py` and `api.py` are routed.

### User accounts with flask-login ###

### Config ###
The file `config.py` includes configuration parameters for the Flask app. There are several different config classes present as you will see. This is because you generally want to have a different configuration for the production server that is user-facing vs the development server that you are running locally (you don't want someone to get a stacktrace in their browser when your server has a bug for example).

Which configuration file to use, what database url to use, and potentially other per-server environmental parameters are set as unix/linux environmental variables. You set these up in the terminal with commands like `export $ENV_VARIABLE=this`, you can see all the environmental variables that are set with the command `env`. A good way to set these environmental variables is to connect them to your python virtualenv by adding them to the file $VIRTUAL_ENV/bin/postactivate. Mine looks like this:
```
#!/bin/zsh
# This hook is sourced after this virtualenv is activated.
export DATABASE_URL="postgresql://localhost/rova"
export APP_SETTINGS="config.DevelopmentConfig"
```

### Manager ###
The file `manage.py` includes commands for useful things you will want to do like migrating the database, running a local server, and compiling client-side javascript (see below). To run a command `python manage.py commandname`.

### Views ###
Routes in `views.py` are what the browser requests to get HTML and the starting point for actually loading a graphical page. These routes should take HTML requests and respond with HTML (unlike the API which speaks JSON). If you want to do server-side rendering of the page, you basically want to write a template file in Jade (see docs), query the data you need to render the page from the database, and then "render" the template with the data before returning it as HTML. If you want to do more client-side rendering of the page, you want to write a minimal template file that includes the appropriate Javascript file which will then request data from the API and render itself. Both are good options.

### API ###
The idea behind having an api which is the interface to all interactions with your database is that you can very carefully and explicitly control what is allowed, and what is not allowed. Your webapp can talk to your server, and so can anything else that is connected to the internet, but by designing the api well, they can only do things they are allowed to do. There are currently three operations that the api provides. Some people have thought a lot about how to build a good API (probably more than is reasonable) and have come up with a concept called a REST or RESTful API which leverages some of the old-as-time design principles behind the internet and the way HTTP works. Might be something worth looking at, but not really a big deal.

When you return an object in your database with the API, do it by writing a `to_dict` function in the model class that returns a python dictionary of fields which you then turn into a json string with the function `jsonify`.

#### Status Codes and Exceptions ####
One thing that is a pretty important for an API is that it return meaningful status codes. When a server sends a response to an HTTP request it includes one of these (http://httpstat.us/) status codes. If there is an error its 4.., if it's a success it's 2... The 3.. status codes are for directing a browser to do something like redirect (these you usually wouldn't send in a JSON API because a JSON API isn't necessarily talking to a browser). You don't send 5.. status codes from your sever on purpose; they indicate that something is seriously wrong with the your server.

I setup an exception handler for the api routes which will turn a raised APIException into a 400 response. See `login()` as an example of how that works.

## Client ##
Definitely do some kind of tutorial for javascript or watch video lectures, I hear Crockford's videos are good. Javascript has some weird parts that are pretty confusing if you don't understand them pretty well, especially in terms of how it treats variable scope, closures, classes, and the keyword "this." (e.g. "this" ALWAYS refers to the function scope that you are closest to, so if you are writing a function inside another function and reference "this" you are referencing the inner function not the outer function, this can really mess you up if you don't understand it).

### "Compiling" client-side code with browserify/uglify ###
Handling variable scope and importing things between separate files and from existing javascript modules is a nightmare in general. Unlike python which decided to be reasonable and define a module/package system and then have a system for importing those packages using a keyword called `import`, nothing like that is specified in the Javascript language. A few competing ways of handling this came about. One is called CommonJS, another AMD, and another RequireJS. You can read about these if you want to. CommonJS is the most reasonable I think, and is what is used when you write Node Javascript code to execute on a server. The way it works is in your javascript file, you specify a global variable called `module.exports`, and then when another file calls `var importedexporthing = require(filname.js)` `importedexportthing` is whatever `module.exports` was set to. The problem is that you can't do it like that in the Browser because of reasons. One way to deal with this problem is called `browserify`. It basically allows you to write javascript as if it was going to execute in Node using the CommonJS and `require` statments and all that, and before you ship the code to the server, you "compile" it all into one machine-generated javascript file which searches embeds all the files you "required" and scopes their variables so they don't conflict with eachother.

I set it up in this repository and made a manage command to run the compilation.
```
python mange.py cc
```
Take a look at the command in `manage.py` to see how it works and see how to modify it.

### Client-side Framework Options ###


## Deploying for reals ##
Cross this bridge when you come to it! Heroku might be a good option for a python server like this.
