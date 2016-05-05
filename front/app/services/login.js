angular.module('prescrisurApp.loginServices', [])

.factory("LogoutService", [
	'$state',
	'AuthService',

	function($state, AuthService) {
		return AuthService.logout().then(function () {
			$state.go('home');
		});
	}
])

.factory('AuthService', ['$q', '$timeout', '$http',
function ($q, $timeout, $http) {

	// create user variable
	var user = null;
	function isLoggedIn() {
		return user ? true : false;
	}

	function register(name, email, password) {
		// create a new instance of deferred
		var deferred = $q.defer();

		// send a post request to the server
		$http.post('/api/register', {name: name, _id: email, password: password})
			// handle success
			.success(function (data, status) {
				if(status === 200 && data.success){
					deferred.resolve();
				} else {
					deferred.reject();
				}
			})
			// handle error
			.error(function (data) {
				deferred.reject();
			});

		// return promise object
		return deferred.promise;

	}

	function login(email, passwd) {
		// create a new instance of deferred
		var deferred = $q.defer();

		// send a post request to the server
		$http.post('/api/login', {email: email, passwd: passwd})
			// handle success
			.success(function (data, status) {
				if(status === 200 && data.data){
					user = data.data;
					deferred.resolve(user);
				} else {
					user = null;
					deferred.reject();
				}
			})
			// handle error
			.error(function () {
				user = null;
				deferred.reject();
			});

		// return promise object
		return deferred.promise;
	}

	function logout() {
		// create a new instance of deferred
		var deferred = $q.defer();

		// send a get request to the server
		$http.get('/api/logout')
			// handle success
			.success(function (data) {
				user = null;
				deferred.resolve();
			})
			// handle error
			.error(function () {
				user = null;
				deferred.reject();
			});

		// return promise object
		return deferred.promise;
	}

	function getUser() {
		var deferred = $q.defer();

		$http.get('/api/me')
			// handle success
			.success(function (data) {
				user = data.user;
				deferred.resolve(user);
			})
			// handle error
			.error(function () {
				user = null;
				deferred.reject();
			});

		return deferred.promise;
	}

	// return available functions for use in controllers
	return ({
		isLoggedIn: isLoggedIn,
		login: login,
		logout: logout,
		register: register,
		getUser: getUser
	});
}]);