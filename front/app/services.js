angular.module('prescrisurApp.services', ['ngResource'])

.factory('Substance', ['$resource',
	function($resource){
		return $resource('http://localhost:5000/api/substances/:id');
	}
])

.factory('Search', ['$resource',
	function($resource){
		return $resource('http://localhost:5000/api/speciality/search');
	}
]);
