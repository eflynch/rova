var React = require('react');
var JQuery = require('jquery');
var $ = require('jquery');
var _ = require('underscore');

var ra = React.DOM;

// Main React component (this is the site)
var Main = React.createClass({
    // Function that sets the this.state object to
    // include the lies object passed in by main function
    // this.state.fetching is used to indicate whether
    // the UI should block while data is being fetched
    getInitialState: function (){
        return {
            lies: this.props.initLies,
            fetching: false
        }
    },
    // Function to fetch most recent lies data
    fetchData: _.debounce(function (){
        var _this = this;
        var lies = this.state.lies;
        lies.fetch().done(function (){
            _this.setState({
                lies: lies,
                fetching: false
            });
        });
    }, 100),
    render: function (){
       return ra.div(null,
            ra.h1(null, "Hello World"),
            ra.p(null, "This is a paragraph"),
            ra.p(null, "This is another paragraph")
       ); 
    }
});

// "main" function
var main = function (){
    // Instantiate client-side models
    var lies = new models.Lies();

    // Fetch models
    // -> on done, mount main react component
    lies.fetch().done(function (){
        var $content = $('.content');
        React.renderComponent(
            Main({initLies: lies}),
            $content[0]
        );
    });
};

// Execute "main" on document ready
$(document).ready(main);
