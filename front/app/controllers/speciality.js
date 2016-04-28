angular.module('prescrisurApp.controllers')

.controller("SpecialityController", [
	'$scope',
	'$window',
	'$stateParams',

	function($scope, $window, $stateParams) {
		$window.location.replace('http://base-donnees-publique.medicaments.gouv.fr/extrait.php?specid='+$stateParams.id);
	}
]);