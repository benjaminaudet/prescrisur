angular.module('prescrisurApp.controllers')

.controller("UserAdminController", [
	'$scope',
	'UserService',
	
	function($scope, UserService) {
		UserService.get(function(data) {
			$scope.users = data.data;
		});

		$scope.isAdmin = function(userRoles) {
			if(userRoles.indexOf('admin') > -1) {
				return true;
			}
			return false;
		};
	}
]);