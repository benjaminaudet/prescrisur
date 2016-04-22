angular.module('prescrisurApp.modelServices', ['ngResource'])

.factory("SpecialityService", [
	'$window',
	'$stateParams',

	function($window, $stateParams) {
		return $window.location.href = 'http://base-donnees-publique.medicaments.gouv.fr/extrait.php?specid='+$stateParams.id;
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