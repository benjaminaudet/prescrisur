var app = angular.module('prescrisurApp', [
	'ngRoute',
	'prescrisurApp.modelServices',
	'prescrisurApp.loginServices',
	'prescrisurApp.controllers'
]);

angular.module('prescrisurApp.controllers', []);


app.config(function($routeProvider, $locationProvider) {
	$routeProvider
		// route for the home page
		.when('/', {
			controller : 'HomeController',
			templateUrl: 'front/app/templates/home.html',
			access: {restricted: false}
		})
		.when('/login', {
			controller : 'LoginController',
			templateUrl: 'front/app/templates/login.html',
			access: {restricted: false}
		})
		.when('/logout', {
			resolve: {controller : 'LogoutService'},
			access: {restricted: true}
		})
		.when('/specialities/:id', {
			resolve: {controller : 'SpecialityService'},
			access: {restricted: true}
		})
		.when('/substances/:id', {
			controller: 'SubstanceController',
			templateUrl: 'front/app/templates/substance.html',
			access: {restricted: true}
		})
		.when('/pathologies/new', {
			controller: 'PathologyEditController',
			templateUrl: 'front/app/templates/pathology-edit.html',
			access: {restricted: true}
		})
		.when('/pathologies/:id', {
			controller: 'PathologyController',
			templateUrl: 'front/app/templates/pathology.html',
			access: {restricted: true}
		})
		.otherwise({redirectTo: '/'});

		// enable HTML5mode to disable hashbang urls
		//$locationProvider.html5Mode(true);
});

app.run(function ($rootScope, $location, $route, AuthService) {
	var postLogInRoute;
	$rootScope.$on('$routeChangeStart',
		function (event, next, current) {
			AuthService.getUser().then(function(user){
				if(next.access.restricted && !AuthService.isLoggedIn()) {
					postLogInRoute = $location.path();
					$location.path('/login');
					return $route.reload();
				} else if(postLogInRoute && AuthService.isLoggedIn()) {
					$location.path(postLogInRoute);
					postLogInRoute = null;
				}
				$rootScope.setCurrentUser(user);
			});
		});
});