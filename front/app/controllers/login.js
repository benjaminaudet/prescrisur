angular.module('prescrisurApp.controllers')

.controller("LogoutController", [
	'$state',
	'AuthService',

	function($state, AuthService) {
		AuthService.logout().then(function () {
			$state.go('home', {msg: 'Déconnecté !'}, {reload: true});
		});
	}
])


.controller("LoginController", [
	'$scope',
	'$state',
	'$stateParams',
	'AuthService',

	function($scope, $state, $stateParams, AuthService) {
		$scope.loginForm = {};
		$scope.needLogin = $stateParams.needLogin;

		if($scope.currentUser) {
			setTimeout(function() { $state.go('home'); }, 1500);
		}

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
				})
				// handle error
				.catch(function () {
					$scope.error = true;
					$scope.disabled = false;
				});
		};
	}
])


.controller("RegisterController", [
	'$scope',
	'$state',
	'AuthService',

	function($scope, $state, AuthService) {
		$scope.registerForm = {};

		if($scope.currentUser) {
			setTimeout(function() { $state.go('home'); }, 1500);
		}

		$scope.checkPassword = function() {
			var password = $scope.registerForm.passwd;
			var confirm = $scope.registerForm.confirmPasswd;
			if (password != '' && password != confirm) {
				$scope.badConfirmPasswd = true;
			} else {
				$scope.badConfirmPasswd = false;
			}
			return !$scope.badConfirmPasswd;
		};

		$scope.register = function () {
			// initial values
			$scope.error = false;
			$scope.disabled = true;
			
			if($scope.checkPassword()) {
				// call login from service
				AuthService.register($scope.registerForm.name, $scope.registerForm.email, $scope.registerForm.passwd)
					// handle success
					.then(function () {
						$scope.registered = true;
						$scope.disabled = false;
					})
					// handle error
					.catch(function () {
						$scope.error = true;
						$scope.disabled = false;
					});
			} else {
				$scope.disabled = false;
			}
		};
	}
]);