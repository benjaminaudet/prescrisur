var app = angular.module('prescrisurApp', [
	'ui.router',
	'ui.select',
	'ui.bootstrap',
	'ngSanitize',
	'prescrisurApp.modelServices',
	'prescrisurApp.loginServices',
	'prescrisurApp.controllers'
]);

angular.module('prescrisurApp.controllers', []);


app.config(function($stateProvider, $urlRouterProvider) {

	$urlRouterProvider.otherwise('/');

	$stateProvider
		.state('home', {
			url: '/',
			controller : 'HomeController',
			templateUrl: 'front/app/templates/home.html',
			access: {restricted: false}
		})
		.state('test', {
			url: '/test',
			controller: 'HomeController',
			templateUrl: 'front/app/templates/test.html',
			access: {restricted: false}
		})
		.state('login', {
			url: '/login',
			controller : 'LoginController',
			templateUrl: 'front/app/templates/login.html',
			access: {restricted: false}
		})
		.state('logout', {
			url: '/logout',
			resolve: {controller : 'LogoutService'},
			access: {restricted: true}
		})
		.state('pathologies-edit', {
			url: '/pathologies/edit/:id',
			controller: 'PathologyEditController',
			templateUrl: 'front/app/templates/pathology-edit.html',
			access: {restricted: true}
		})
		.state('pathologies-new', {
			url: '/pathologies/new',
			controller: 'PathologyEditController',
			templateUrl: 'front/app/templates/pathology-edit.html',
			access: {restricted: true}
		})
		.state('pathologies', {
			url: '/pathologies/:id',
			controller: 'PathologyController',
			templateUrl: 'front/app/templates/pathology.html',
			access: {restricted: true}
		})
		.state('specialities', {
			url: '/specialities/:id',
			templateUrl: 'front/app/templates/speciality.html',
			access: {restricted: false},
			external: 'http://base-donnees-publique.medicaments.gouv.fr/extrait.php?specid='
		})
		.state('substances', {
			url: '/substances/:id',
			controller: 'SubstanceController',
			templateUrl: 'front/app/templates/substance.html',
			access: {restricted: true}
		})
});

app.run(function ($rootScope, $state, $window, AuthService) {
	var postLoginState, postLoginParams;
	$rootScope.$on('$stateChangeStart',
		function (event, toState, toParams) {
			AuthService.getUser().then(function(user){
				if(toState.access.restricted && !AuthService.isLoggedIn()) {
					postLoginState = $state.current.name;
					postLoginParams = $state.params;
					return $state.go('login');
				} else if(postLoginState && AuthService.isLoggedIn()) {
					$state.go(postLoginState, postLoginParams);
					postLoginState = null;
					postLoginParams = null;
				}
				$rootScope.setCurrentUser(user);

				// Redirect to external URL
				if (toState.external) {
					event.preventDefault();
					$window.open(toState.external+$state.params.id, '_self');
				}
			});
		});
});