angular.module('prescrisurApp.modelServices', ['ngResource'])

.factory('PathologyService', ['$resource',
	function($resource){
		return $resource('/api/pathologies/:id', null, {
			update: { method:'PUT' }
		});
	}
])

.factory('SubstanceService', ['$resource',
	function($resource){
		return $resource('/api/substances/:id');
	}
])

.factory('SearchService', ['$resource',
	function($resource){
		return $resource('/api/:searchType/search');
	}
]);