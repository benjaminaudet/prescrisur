angular.module('prescrisurApp.controllers')

.controller("SpecialityController", [
	'$scope',
	'$routeParams',

	function($scope, $routeParams) {
		window.location.href = 'http://base-donnees-publique.medicaments.gouv.fr/extrait.php?specid='+$routeParams.id;
	}
]);
