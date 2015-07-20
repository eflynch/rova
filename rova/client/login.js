var React = require('react');
var JQuery = require('jquery');
var $ = require('jquery');

var Header = require('./header').Header;

var ra = React.DOM;

var login = function (){
    var username = $('.username').val();
    var password = $('.password').val();
    return $.ajax('/api/login',{
        data: JSON.stringify({
            username: username,
            password: password
        }),
        contentType: 'application/json',
        type: 'POST'
    }); 
};

// LoginMain React component (this is the site)
var LoginMain = React.createClass({
    getInitialState: function (){
        return {
            working: false,
            error: false
        }
    },
    login: function (){
        var that = this;
        that.setState({working: true});
        login()
        .done(function(){
            window.location = '/';
        })
        .fail(function (){
            that.setState({error: true, working: false});
            setTimeout(function (){ that.setState({error: false});}, 4000);
        })
    },
    loginHandler: function (e){
        if (e.key === 'Enter'){
            e.target.blur();
            this.login();
        }
    },
    signupHandler: function (){

    },
    render: function (){
       return ra.div(null,
            React.createElement(Header, {
                username: this.props.username
            }),
            ra.form(null,
                ra.input({
                    className: 'username',
                    placeholder: 'username',
                    type: 'text',
                    onKeyDown: function (e){
                        if (e.key == 'Enter'){
                            $('.password').focus();
                        }
                    }
                }),
                ra.input({
                    className: 'password',
                    placeholder: 'password',
                    type: 'password',
                    onKeyDown: this.loginHandler
                })
            )
       ); 
    }
});

// "main" function
var main = function (){
    var $content = $('.content');
    React.render(
        React.createElement(LoginMain, null),
        $content[0]
    );
};

// Execute "main" on document ready
$(document).ready(main);
