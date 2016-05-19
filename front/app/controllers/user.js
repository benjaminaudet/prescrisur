angular.module('prescrisurApp.controllers')
	
	
.controller("UserController", [
	'$scope',
	'Flash',
	'AuthService',

	function($scope, Flash, AuthService) {
		$scope.me = {name: $scope.currentUser.name};

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
				.then(function () {
					Flash.create('success', 'Profil mis à jour !');
					$scope.disabled = false;
				})
				.catch(function (error) {
					if(error.bad_password) {
						Flash.create('danger', 'Le mot de passe est incorrect.', 0);
					}
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
	
	function($scope, $state, Flash, filterFilter, PageTitleService, UserService, UserSubscriptionService) {
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
			
			if (subscribe) {
				UserSubscriptionService.subscribe({ id: user._id }, {}, afterSave(user.name + ' abonné !'));
			} else {
				UserSubscriptionService.unsubscribe({ id: user._id }, afterSave(user.name + ' désabonné !'));
			}
		}
	}
]);