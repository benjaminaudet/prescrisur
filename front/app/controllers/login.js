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
	'PageTitleService',
	'AuthService',

	function($scope, $state, $stateParams, PageTitleService, AuthService) {
		PageTitleService.setTitle('Connexion');

		$scope.loginForm = {};
		$scope.needLogin = $stateParams.needLogin;

		if($scope.currentUser) {
			setTimeout(function() { $state.go('home'); }, 1500);
		}
		
		$scope.sendConfirmation = function() {
			AuthService.confirm($scope.loginForm.email)
				.then(function() {
					$scope.confirmSent = true;
					$scope.error = false;
					$scope.confirmAgain = true;
				})
				.catch(function() {
					$scope.error = "Problème dans l'envoi de la confirmation...";
					$scope.confirmAgain = true;
				});
		};

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
				.catch(function (error) {
					if(error.error) {
						$scope.error = error.error;
					} else if (error.bad_password) {
						$scope.error = 'Mauvais login/mot de passe !';
					} else if (error.not_confirmed) {
						$scope.error = "Votre compte n'a pas été confirmé !";
						$scope.confirmAgain = true;
					}
					$scope.disabled = false;
				});
		};
	}
])
	

.controller("ResetPasswordController", [
	'$scope',
	'$state',
	'$stateParams',
	'$timeout',
	'Flash',
	'AuthService',

	function($scope, $state, $stateParams, $timeout, Flash, AuthService) {
		$scope.resetForm = {};
		
		if($stateParams.token) {
			AuthService.checkResetPassword($stateParams.token)
				.then(function (data) {
					$scope.resetConfirmed = true;
					$scope.resetForm.email = data.email;
				})
				// handle error
				.catch(function (error) {
					if(error.error) {
						Flash.create('danger', "Le code de confirmation est erroné. Merci de recommencer.", 0)
					}
				});
		}

		$scope.checkPassword = function() {
			var password = $scope.resetForm.passwd;
			var confirm = $scope.resetForm.confirmPasswd;
			if (password != '' && password != confirm) {
				$scope.badConfirmPasswd = true;
				$scope.disabled = true;
			} else {
				$scope.badConfirmPasswd = false;
				$scope.disabled = false;
			}
			return !$scope.badConfirmPasswd;
		};

		$scope.resetPassword = function() {
			// initial values
			$scope.error = false;
			$scope.disabled = true;

			AuthService.resetPassword($scope.resetForm.email, $scope.resetForm.passwd)
				.then(function () {
					Flash.create('success', 'Votre mot de passe a bien été changé ! Redirection...');
					$timeout(function () { $state.go('login'); }, 1500);
				})
				// handle error
				.catch(function (error) {
					if(error.error) {
						Flash.create('danger', "Aucun utilisateur avec cette adresse n'est enregistré !", 0);
					}
				});
		};

		$scope.sendReset = function() {
			// initial values
			$scope.error = false;
			$scope.disabled = true;

			AuthService.sendPasswordResetMail($scope.resetForm.email)
			// handle success
				.then(function () {
					Flash.create('success', 'Un mail vient de vous êtes envoyé à '+ $scope.resetForm.email +'. Suivez le lien pour réinitialiser votre mot de passe.');
					$scope.disabled = false;
				})
				// handle error
				.catch(function (error) {
					if(error.no_user) {
						Flash.create('danger', "Aucun utilisateur avec cette adresse n'est enregistré !", 0);
					} else if(error.not_confirmed) {
						Flash.create('danger', "Cet utilisateur n'a pas confirmé son adresse email, merci de confirmer l'adresse : " + $scope.resetForm.email, 0);
					}
					$scope.disabled = false;
				});
		}
	}
])
	
	
.controller("RegisterController", [
	'$scope',
	'$state',
	'PageTitleService',
	'PageService',
	'AuthService',

	function($scope, $state, PageTitleService, PageService, AuthService) {
		PageTitleService.setTitle('Inscription');

		$scope.registerForm = {};

		if($scope.currentUser) {
			setTimeout(function() { $state.go('home'); }, 1500);
		}
		
		PageService.get({id : 'inscription'}, function(data) {
			$scope.text = data.data;
		});

		$scope.checkPassword = function() {
			var password = $scope.registerForm.passwd;
			var confirm = $scope.registerForm.confirmPasswd;
			if (password != '' && password != confirm) {
				$scope.badConfirmPasswd = true;
				$scope.disabled = true;
			} else {
				$scope.badConfirmPasswd = false;
				$scope.disabled = false;
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
					.catch(function (error,a,b,c) {
						if(error.error) {
							$scope.error = error.error;
						} else if (error.already_exist) {
							$scope.error = 'Un compte existe déjà avec cette adresse mail !';
						}
						$scope.disabled = false;
					});
			} else {
				$scope.disabled = false;
			}
		};
	}
]);