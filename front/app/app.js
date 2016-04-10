var app = angular.module('prescrisurApp', [
	'ngRoute',
	'prescrisurApp.controllers'
]);

angular.module('prescrisurApp.controllers', []);


app.config(function($routeProvider, $locationProvider) {
	$routeProvider
		// route for the home page
		.when('/', {
			templateUrl: 'app/templates/welcome.html',
			controller : 'MainController'
		})
		.when('/specialities/:id', {
			controller: 'SpecialityController',
			templateUrl: 'app/templates/welcome.html'
		})
		.otherwise({redirectTo: '/'});

		// enable HTML5mode to disable hashbang urls
		$locationProvider.html5Mode(true);
});