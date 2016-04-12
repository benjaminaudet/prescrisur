angular.module('prescrisurApp.controllers')

.controller("MainController", [
	'$scope',
	'$rootScope',

	function($scope, $rootScope) {
		$scope.currentUser = null;

		$rootScope.setCurrentUser = function(user) {
			$scope.currentUser = user;
		}
	}
]);