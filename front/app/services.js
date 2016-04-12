angular.module('prescrisurApp.services', ['ngResource'])

.factory('Substance', ['$resource',
	function($resource){
		return $resource('/api/substances/:id');
	}
])

.factory('Search', ['$resource',
	function($resource){
		return $resource('/api/speciality/search');
	}
]);
