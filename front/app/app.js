var app = angular.module('prescrisurApp', [
	'ngRoute',
	'prescrisurApp.controllers',
	'prescrisurApp.services'
]);

angular.module('prescrisurApp.controllers', []);


app.config(function($routeProvider, $locationProvider) {
	$routeProvider
		// route for the home page
		.when('/', {
			controller : 'MainController',
			templateUrl: 'front/app/templates/welcome.html'
		})
		.when('/specialities/:id', {
			controller: 'SpecialityController',
			templateUrl: 'front/app/templates/welcome.html'
		})
		.when('/substances/:id', {
			controller: 'SubstanceController',
			templateUrl: 'front/app/templates/substance.html'
		})
		.otherwise({redirectTo: '/'});

		// enable HTML5mode to disable hashbang urls
		//$locationProvider.html5Mode(true);
});