angular.module('prescrisurApp.controllers')
	
	
.controller("UserController", [
	'$scope',
	'Flash',
	'AuthService',

	function($scope, Flash, AuthService) {
		$scope.$watch('currentUser', function(user) {
			$scope.me = {name: user.name, email: user.email};
		});

		$scope.checkPassword = function() {
			var password = $scope.me.newPasswd;
			var confirm = $scope.me.confirmNewPasswd;
			if (password != '' && password != confirm) {
				$scope.badConfirmPasswd = true;
				$scope.disabled = true;
			} else {
				$scope.badConfirmPasswd = false;
				$scope.disabled = false;
			}
			return !$scope.badConfirmPasswd;
		};
		
		$scope.submit = function() {
			$scope.error = false;
			$scope.disabled = true;
			
			AuthService.updateUser($scope.me)
				.then(function (data) {
					if(data.updated_mail) {
						Flash.create('info', "Un mail de confirmation vient d'être envoyé à "+ data.updated_mail +" pour valider le changement d'adresse email", 0);
					}
					Flash.create('success', 'Profil mis à jour !');
					$scope.disabled = false;
					$scope.currentUser = data.user;
				})
				.catch(function (error) {
					var msg = 'Une erreur est survenue...';
					if(error.bad_password) {
						msg = 'Le mot de passe est incorrect';
					}
					Flash.create('danger', msg, 10000);
					$scope.disabled = false;
				});
		};
	}
])
	
	
.controller("UserAdminController", [
	'$scope',
	'$state',
	'Flash',
	'filterFilter',
	'PageTitleService',
	'UserService',
	'UserSubscriptionService',
	'UserNewsletterService',
	
	function($scope, $state, Flash, filterFilter, PageTitleService, UserService, UserSubscriptionService, UserNewsletterService) {
		PageTitleService.setTitle('Administration des Utilisateurs');

		UserService.get(function(data) {
			$scope.users = data.data;
			$scope.subscribers = filterFilter(data.data, { roles: 'subscriber' });
		});

		$scope.hasRole = function(role, userRoles) {
			return userRoles.indexOf(role) > -1;
		};
		
		$scope.subscribe = function(user, subscribe) {
			var afterSave = function(msg) {
				return function() {
					Flash.create('success', msg);
					$state.go('users', {}, {reload: true});
				}
			};

			var afterError = function() {
				Flash.create('danger', 'Une erreur est survenue...', 10000);
			};
			
			if (subscribe) {
				UserSubscriptionService.subscribe({ id: user._id }, {}, afterSave(user.name + ' abonné premium !'), afterError);
			} else {
				UserSubscriptionService.unsubscribe({ id: user._id }, afterSave(user.name + ' désabonné premium !'), afterError);
			}
		}

		$scope.newsletter = function(user, subscribe) {
			var afterSave = function(msg) {
				return function() {
					Flash.create('success', msg);
					$state.go('users', {}, {reload: true});
				}
			};

			var afterError = function() {
				Flash.create('danger', 'Une erreur est survenue...', 10000);
			};
			
			if (subscribe) {
				UserNewsletterService.subscribe({ id: user._id }, {}, afterSave(user.name + ' abonné à la newsletter !'), afterError);
			} else {
				UserNewsletterService.unsubscribe({ id: user._id }, afterSave(user.name + ' désabonné de la newsletter !'), afterError);
			}
		}
	}
]);