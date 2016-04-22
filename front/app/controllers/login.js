angular.module('prescrisurApp.controllers')

.controller("LoginController", [
	'$scope',
	'$state',
	'AuthService',

	function($scope, $state, AuthService) {

		$scope.login = function () {
			// initial values
			$scope.error = false;
			$scope.disabled = true;

			// call login from service
			AuthService.login($scope.loginForm.email, $scope.loginForm.passwd)
				// handle success
				.then(function (user) {
					$state.go('home');
					$scope.disabled = false;
					$scope.loginForm = {};
				})
				// handle error
				.catch(function () {
					$scope.error = true;
					$scope.errorMessage = "Invalid username and/or password";
					$scope.disabled = false;
					$scope.loginForm = {};
				});
		};
	}
]);