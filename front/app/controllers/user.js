angular.module('prescrisurApp.controllers')

.controller("UserAdminController", [
	'$scope',
	'$state',
	'Flash',
	'filterFilter',
	'UserService',
	'UserSubscriptionService',
	
	function($scope, $state, Flash, filterFilter, UserService, UserSubscriptionService) {
		UserService.get(function(data) {
			$scope.users = data.data;
			$scope.subscribers = filterFilter(data.data, { roles: 'subscriber' });
		});

		$scope.hasRole = function(role, userRoles) {
			if(userRoles.indexOf(role) > -1) {
				return true;
			}
			return false;
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