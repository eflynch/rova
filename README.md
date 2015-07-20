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
The database I recommend is postgresql because it's easy to setup and feature-rich.

### Creating / Deleting databases ###

### Querying database ###

### Sqlalchemy ###

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

### Client-side Framework Options ###

## Deploying for reals ##
Cross this bridge when you come to it! Heroku might be a good option for a python server like this.
