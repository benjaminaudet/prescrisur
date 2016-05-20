var app = angular.module('prescrisurApp', [
	'ui.router',
	'ui.select',
	'ui.bootstrap',
	'ngFlash',
	'colorpicker.module',
	'yaru22.angular-timeago',
	'textAngular',
	'ngSanitize',
	'templates',
	'prescrisurApp.commonsServices',
	'prescrisurApp.modelServices',
	'prescrisurApp.loginServices',
	'prescrisurApp.directives',
	'prescrisurApp.controllers'
]);

angular.module('prescrisurApp.controllers', []);

// Routing
app.config(function($stateProvider, $urlRouterProvider) {

	$urlRouterProvider.otherwise('/');

	$stateProvider
		.state('home', {
			url: '/',
			controller : 'HomeController',
			templateUrl: 'home.html',
			params: {msg: null},
			access: {restricted: false}
		})
		// Pathologies
		.state('pathologies-new', {
			url: '/pathologies/new',
			controller: 'PathologyEditController',
			templateUrl: 'pathology-edit.html',
			access: {restricted: true, admin: true}
		})
		.state('pathologies', {
			url: '/pathologies/:id',
			controller: 'PathologyController',
			templateUrl: 'pathology.html',
			access: {restricted: false}
		})
			.state('pathologies.edit', {
				url: '/edit',
				views: {
					'@': {
						controller: 'PathologyEditController',
						templateUrl: 'pathology-edit.html'
					}
				},
				access: {restricted: true, admin: true}
			})
		// Classes
		.state('classes', {
			url: '/classes/:id',
			controller: 'TherapeuticClassController',
			templateUrl: 'therapeutic-class.html',
			access: {restricted: false}
		})
		// Specialities
		.state('specialities', {
			url: '/specialities/:id',
			controller: 'SpecialityController',
			templateUrl: 'speciality.html',
			access: {restricted: false}
		})
		// Substances
		.state('substances', {
			url: '/substances/:id',
			controller: 'SubstanceController',
			templateUrl: 'substance.html',
			access: {restricted: true}
		})
		// Associations
		.state('associations', {
			url: '/associations',
			controller: 'AssociationController',
			templateUrl: 'association.html',
			params: {msg: null},
			access: {restricted: true, admin: true}
		})
		// Users
		.state('users', {
			url: '/users',
			controller: 'UserAdminController',
			templateUrl: 'user-admin.html',
			access: {restricted: true, admin: true}
		})
		.state('register', {
			url: '/register',
			controller : 'RegisterController',
			templateUrl: 'register.html',
			access: {restricted: false}
		})
		.state('login', {
			url: '/login',
			controller : 'LoginController',
			templateUrl: 'login.html',
			params: {needLogin: false},
			access: {restricted: false}
		})
		.state('profile', {
			url: '/me',
			controller : 'UserController',
			templateUrl: 'user-edit.html',
			access: {restricted: true}
		})
		.state('logout', {
			url: '/logout',
			controller: 'LogoutController',
			template: '',
			access: {restricted: true}
		})
		.state('reset-password', {
			url: '/reset/:token',
			controller : 'ResetPasswordController',
			templateUrl: 'reset-password.html',
			access: {restricted: false}
		})
		// Pages
		.state('pages', {
			url: '/pages',
			controller: 'PageController',
			templateUrl: 'page-admin.html',
			access: {restricted: true, admin: true}
		})
			.state('pages.new', {
				url: '/new',
				views: {
					'@': {
						controller: 'PageEditController',
						templateUrl: 'page-edit.html'
					}
				},
				access: {restricted: true, admin: true}
			})
			.state('pages.read', {
				url: '/:id',
				views: {
					'@': {
						controller: 'PageController',
						templateUrl: 'page.html'
					}
				},
				access: {restricted: false}
			})
			.state('pages.edit', {
				url: '/:id/edit',
				views: {
					'@': {
						controller: 'PageEditController',
						templateUrl: 'page-edit.html'
					}
				},
				access: {restricted: true, admin: true}
			})
		.state('contact', {
			url: '/contact',
			controller: 'ContactController',
			templateUrl: 'contact.html',
			access: {restricted: false}
		})
		// News
		.state('news', {
			url: '/news',
			controller: 'NewsController',
			templateUrl: 'news.html',
			access: {restricted: false}
		})
			.state('news.new', {
				url: '/new',
				views: {
					'@': {
						controller: 'NewsEditController',
						templateUrl: 'news-edit.html'
					}
				},
				access: {restricted: true, admin: true}
			})
			.state('news.read', {
				url: '/:id',
				views: {
					'@': {
						controller: 'NewsController',
						templateUrl: 'news.html'
					}
				},
				access: {restricted: false}
			})
			.state('news.edit', {
				url: '/:id/edit',
				views: {
					'@': {
						controller: 'NewsEditController',
						templateUrl: 'news-edit.html'
					}
				},
				access: {restricted: true, admin: true}
			})
		.state('error', {
			url: '/error',
			controller : 'ErrorController',
			templateUrl: 'error.html',
			params: {code: null},
			access: {restricted: false}
		})
});

// On route change
app.run(function ($rootScope, $state, $window, ConfirmQuitService, AuthService) {
	var postLoginState, postLoginParams;
	$rootScope.$on('$stateChangeStart',
		function (event, toState, toParams) {
			// Prevent confirm before quit to run on all pages
			ConfirmQuitService.destroyWindowQuit();

			// Authenticate user
			AuthService.getUser()
				.then(function(user) {
					if(postLoginState && AuthService.isLoggedIn()) {
						$state.go(postLoginState, postLoginParams);
						postLoginState = null;
						postLoginParams = null;
					} else if(toState.access.admin && user.roles.indexOf('admin') == -1) {
						return $state.go('error', {code: 403});
					}
					$rootScope.setCurrentUser(user);
				})
				.catch(function(e) {
					if(e.need_login || toState.access.restricted) {
						postLoginState = $state.current.name;
						postLoginParams = $state.params;
						return $state.go('login', {needLogin: true});
					} else if(e.need_role || toState.access.admin) {
						return $state.go('error', {code: 403});
					}
					$rootScope.setCurrentUser(null);
				});
		});
});

// textAngular Setup
app.config(['$provide', function($provide){
	// this demonstrates how to register a new tool and add it to the default toolbar
	$provide.decorator('taOptions', ['$delegate', function(taOptions){
		// $delegate is the taOptions we are decorating
		// here we override the default toolbars and classes specified in taOptions.
		taOptions.forceTextAngularSanitize = true; // set false to allow the textAngular-sanitize provider to be replaced
		taOptions.keyMappings = []; // allow customizable keyMappings for specialized key boards or languages
		taOptions.toolbar = [
			['undo', 'redo'],
			['h2', 'h3', 'h4'],
			['bold', 'italics', 'underline', 'fontColor', 'clear'],
			['justifyLeft','justifyCenter','justifyRight', 'justifyFull'],
			['ul', 'indent', 'outdent'],
			['insertImage', 'insertLink']
		];
		taOptions.classes = {
			focussed: 'focussed',
			toolbar: 'btn-toolbar',
			toolbarGroup: 'btn-group',
			toolbarButton: 'btn btn-default',
			toolbarButtonActive: 'active',
			disabled: 'disabled',
			textEditor: 'form-control',
			htmlEditor: 'form-control'
		};
		return taOptions; // whatever you return will be the taOptions
	}]);

	$provide.decorator('taOptions', ['taRegisterTool', '$delegate', function(taRegisterTool, taOptions){
		// $delegate is the taOptions we are decorating
		// register the tool with textAngular
		taRegisterTool('fontColor', {
			display: "<button colorpicker type='button' class='btn btn-default ng-scope'  title='Font Color'  colorpicker-close-on-select colorpicker-position='bottom' ng-model='fontColor' style='color: {{fontColor}}'><i class='fa fa-font '></i></button>",
			action: function (deferred) {
				var self = this;
				if (typeof self.listener == 'undefined') {
					self.listener = self.$watch('fontColor', function (newValue) {
						self.$editor().wrapSelection('foreColor', newValue);
					});
				}
				self.$on('colorpicker-selected', function () {
					deferred.resolve();
				});
				self.$on('colorpicker-closed', function () {
					deferred.resolve();
				});
				return false;
			}
		});
		//taOptions.toolbar[1].push('fontColor');

		taOptions.setup.textEditorSetup=function($element) {
			$element.attr('ui-codemirror', '');
		};
		return taOptions;
	}]);
}]);