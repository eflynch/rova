var React = require('react');
var $ = require('jquery');

var ra = React.DOM;

var logout = function (){
    return $.ajax('/api/logout',{type: 'POST'});
}

var Header = React.createClass({
    logoutHandler: function (){
        logout()
        .then(function () {window.location = '/login';})
        .fail();
    },
    formatUsername: function (){
        if (!this.props.username){
            return '';
        }
        if (this.props.username.length > 14){
            return 'Hi ' + this.props.username.slice(0, 11) + '...';
        } else {
            return 'Hi ' + this.props.username;
        }
    },
    render: function (){
        if (this.props.username){
            var buttons = ra.div(null,
                ra.a({
                    onClick: this.logoutHandler
                }, 'logout')
            );
        } else {
            var buttons = ra.div(null,
                ra.a({
                    href: '/login'
                }, 'login/signup')
            );
        }
        return ra.div({className: 'header'},
            ra.h1(null, 'ROVA!!'),
            ra.p(null, this.formatUsername()),
            buttons
        );
    }
});

module.exports = {
    Header: Header
};
