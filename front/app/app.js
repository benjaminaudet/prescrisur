var app = angular.module('prescrisurApp', [
	'ui.router',
	'ui.select',
	'ui.bootstrap',
	'ngFlash',
	'colorpicker.module',
	'yaru22.angular-timeago',
	'textAngular',
	'ngSanitize',
	'prescrisurApp.commonsServices',
	'prescrisurApp.modelServices',
	'prescrisurApp.loginServices',
	'prescrisurApp.directives',
	'prescrisurApp.filters',
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
			templateUrl: 'front/app/templates/home.html',
			params: {msg: null},
			access: {restricted: false}
		})
		// Pathologies
		.state('pathologies', {
			url: '/pathologies',
			controller: 'PathologyAdminController',
			templateUrl: 'front/app/templates/pathology-admin.html',
			access: {restricted: true, admin: true}
		})
			.state('pathologies.new', {
				url: '/new',
				views: {
					'@': {
						controller: 'PathologyEditController',
						templateUrl: 'front/app/templates/pathology-edit.html'
					}
				},
				access: {restricted: true, admin: true}
			})
			.state('pathologies.read', {
				url: '/:id?draft',
				views: {
					'@': {
						controller: 'PathologyController',
						templateUrl: 'front/app/templates/pathology.html'
					}
				},
				access: {restricted: false}
			})
			.state('pathologies.edit', {
				url: '/:id/edit?draft',
				views: {
					'@': {
						controller: 'PathologyEditController',
						templateUrl: 'front/app/templates/pathology-edit.html'
					}
				},
				access: {restricted: true, admin: true}
			})
		// Classes
		.state('classes', {
			url: '/classes/:id',
			controller: 'TherapeuticClassController',
			templateUrl: 'front/app/templates/therapeutic-class.html',
			access: {restricted: true}
		})
		// Specialities
		.state('specialities', {
			url: '/specialities/:id',
			controller: 'SpecialityController',
			templateUrl: 'front/app/templates/speciality.html',
			access: {restricted: false}
		})
		// Substances
		.state('substances', {
			url: '/substances/:id',
			controller: 'SubstanceController',
			templateUrl: 'front/app/templates/substance.html',
			access: {restricted: true}
		})
		// Associations
		.state('associations', {
			url: '/associations',
			controller: 'AssociationController',
			templateUrl: 'front/app/templates/association.html',
			params: {msg: null},
			access: {restricted: true, admin: true}
		})
		// Users
		.state('users', {
			url: '/users',
			controller: 'UserAdminController',
			templateUrl: 'front/app/templates/user-admin.html',
			access: {restricted: true, admin: true}
		})
		.state('register', {
			url: '/register',
			controller : 'RegisterController',
			templateUrl: 'front/app/templates/register.html',
			access: {restricted: false}
		})
		.state('login', {
			url: '/login',
			controller : 'LoginController',
			templateUrl: 'front/app/templates/login.html',
			params: {needLogin: false},
			access: {restricted: false}
		})
		.state('profile', {
			url: '/me',
			controller : 'UserController',
			templateUrl: 'front/app/templates/user-edit.html',
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
			templateUrl: 'front/app/templates/reset-password.html',
			access: {restricted: false}
		})
		// Pages
		.state('pages', {
			url: '/pages',
			controller: 'PageController',
			templateUrl: 'front/app/templates/page-admin.html',
			access: {restricted: true, admin: true}
		})
			.state('pages.new', {
				url: '/new',
				views: {
					'@': {
						controller: 'PageEditController',
						templateUrl: 'front/app/templates/page-edit.html'
					}
				},
				access: {restricted: true, admin: true}
			})
			.state('pages.read', {
				url: '/:id',
				views: {
					'@': {
						controller: 'PageController',
						templateUrl: 'front/app/templates/page.html'
					}
				},
				access: {restricted: false}
			})
			.state('pages.edit', {
				url: '/:id/edit',
				views: {
					'@': {
						controller: 'PageEditController',
						templateUrl: 'front/app/templates/page-edit.html'
					}
				},
				access: {restricted: true, admin: true}
			})
		.state('contact', {
			url: '/contact',
			controller: 'ContactController',
			templateUrl: 'front/app/templates/contact.html',
			access: {restricted: false}
		})
		// News
		.state('news', {
			url: '/news',
			controller: 'NewsController',
			templateUrl: 'front/app/templates/news.html',
			access: {restricted: false}
		})
			.state('news.new', {
				url: '/new',
				views: {
					'@': {
						controller: 'NewsEditController',
						templateUrl: 'front/app/templates/news-edit.html'
					}
				},
				access: {restricted: true, admin: true}
			})
			.state('news.read', {
				url: '/:id',
				views: {
					'@': {
						controller: 'NewsController',
						templateUrl: 'front/app/templates/news.html'
					}
				},
				access: {restricted: false}
			})
			.state('news.edit', {
				url: '/:id/edit',
				views: {
					'@': {
						controller: 'NewsEditController',
						templateUrl: 'front/app/templates/news-edit.html'
					}
				},
				access: {restricted: true, admin: true}
			})
		.state('error', {
			url: '/error',
			controller : 'ErrorController',
			templateUrl: 'front/app/templates/error.html',
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