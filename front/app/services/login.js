angular.module('prescrisurApp.loginServices', [])

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
		$http.post('/api/register', {name: name, email: email, password: password})
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
				deferred.reject(data);
			});

		// return promise object
		return deferred.promise;

	}
	
	function confirm(email) {
		// create a new instance of deferred
		var deferred = $q.defer();

		// send a post request to the server
		$http.post('/api/confirm/send', {email: email})
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
				deferred.reject(data);
			});

		// return promise object
		return deferred.promise;
		
	}
	
	function sendPasswordResetMail(email) {
		// create a new instance of deferred
		var deferred = $q.defer();

		// send a post request to the server
		$http.post('/api/reset/send', {email: email})
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
				deferred.reject(data);
			});

		// return promise object
		return deferred.promise;
		
	}
	
	
	function resetPassword(email, passwd) {
		// create a new instance of deferred
		var deferred = $q.defer();

		// send a post request to the server
		$http.post('/api/reset', {email: email, passwd: passwd})
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
				deferred.reject(data);
			});

		// return promise object
		return deferred.promise;
		
	}
	

	function checkResetPassword(token) {
		// create a new instance of deferred
		var deferred = $q.defer();

		// send a post request to the server
		$http.get('/api/reset/'+token)
		// handle success
			.success(function (data, status) {
				if(status === 200){
					deferred.resolve(data);
				} else {
					deferred.reject(data);
				}
			})
			// handle error
			.error(function (data) {
				deferred.reject(data);
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
			.error(function (error) {
				user = null;
				deferred.reject(error);
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
				if(!user) {
					deferred.reject({});
				}
				deferred.resolve(user);
			})
			// handle error
			.error(function (e) {
				user = null;
				deferred.reject(e);
			});

		return deferred.promise;
	}
	
	function updateUser(data) {
		var deferred = $q.defer();

		$http.put('/api/me', data)
		// handle success
			.success(function (data) {
				user = data.user;
				if(!user) {
					deferred.reject({});
				}
				deferred.resolve(user);
			})
			// handle error
			.error(function (e) {
				user = null;
				deferred.reject(e);
			});

		return deferred.promise;
	}

	// return available functions for use in controllers
	return ({
		isLoggedIn: isLoggedIn,
		login: login,
		logout: logout,
		register: register,
		confirm: confirm,
		sendPasswordResetMail: sendPasswordResetMail,
		checkResetPassword: checkResetPassword,
		resetPassword: resetPassword,
		getUser: getUser,
		updateUser: updateUser
	});
}]);