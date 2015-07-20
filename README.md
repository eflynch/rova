# ROVA #

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

## Database ##

### Creating / Deleting databases ###

### Querying database ###

### Migrations ###

## Server ##

### User accounts with flask-login ###

### Config ###

### Manager ###

### Views ###

### API ###

#### Exceptions ####

## Client ##
Definitely do some kind of tutorial for javascript or watch video lectures, I hear Crockford's videos are good. Javascript has some weird parts that are pretty confusing if you don't understand them pretty well, especially in terms of how it treats variable scope, closures, classes, and the keyword "this." (e.g. "this" ALWAYS refers to the function scope that you are closest to, so if you are writing a function inside another function and reference "this" you are referencing the inner function not the outer function, this can really mess you up if you don't understand it).

### "Compiling" client-side code with browserify/uglify ###

## Deploying for reals ##
Cross this bridge when you come to it! Heroku might be a good option for a python server like this.
