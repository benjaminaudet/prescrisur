angular.module('prescrisurApp.controllers')

.controller("MainController", [
	'$scope',
	'$state',
	'$rootScope',

	function($scope, $state, $rootScope) {
		$scope.currentUser = null;

		$rootScope.setCurrentUser = function(user) {
			$scope.currentUser = user;
		};

		$scope.checkPageInfoState = function() {
			if($state.current.name == 'pages') {
				var pagesArray = ['pourquoi-prescrisur', 'presentation'];
				if (pagesArray.indexOf($state.params.id) != -1) {
					return true;
				}
			}
			return false;
		}
	}
]);