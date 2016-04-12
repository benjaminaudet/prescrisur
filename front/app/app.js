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
			controller : 'HomeController',
			templateUrl: 'front/app/templates/welcome.html',
			access: {restricted: false}
		})
		.when('/login', {
			controller : 'LoginController',
			templateUrl: 'front/app/templates/login.html',
			access: {restricted: false}
		})
		.when('/logout', {
			resolve: {controller: 'LogoutController'},
			access: {restricted: true}
		})
		.when('/specialities/:id', {
			controller: 'SpecialityController',
			templateUrl: 'front/app/templates/welcome.html',
			access: {restricted: true}
		})
		.when('/substances/:id', {
			controller: 'SubstanceController',
			templateUrl: 'front/app/templates/substance.html',
			access: {restricted: true}
		})
		.otherwise({redirectTo: '/'});

		// enable HTML5mode to disable hashbang urls
		//$locationProvider.html5Mode(true);
});

app.run(function ($rootScope, $location, $route, Auth) {
	var postLogInRoute;
	$rootScope.$on('$routeChangeStart',
		function (event, next, current) {
			Auth.getUser().then(function(user){
				if(next.access.restricted && !Auth.isLoggedIn()) {
					postLogInRoute = $location.path();
					$location.path('/login');
					$route.reload();
				} else if(postLogInRoute && Auth.isLoggedIn()) {
					$location.path(postLogInRoute);
					postLogInRoute = null;
				}
				$rootScope.setCurrentUser(user);
			});
		});
});