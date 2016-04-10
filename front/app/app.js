var app = angular.module('prescrisurApp', [
	'ngRoute',
	'prescrisurControllers'
]);


app.config(function($routeProvider, $locationProvider) {
	$routeProvider
		// route for the home page
		.when('/', {
			templateUrl : 'app/templates/welcome.html',
			controller  : 'MainController'
		});

		// enable HTML5mode to disable hashbang urls
		$locationProvider.html5Mode(true);
});