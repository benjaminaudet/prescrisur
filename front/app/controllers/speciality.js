angular.module('prescrisurApp.controllers')

.controller("SpecialityController", [
	'$window',
	'$routeParams',

	function($window, $routeParams) {
		$window.location.href = 'http://base-donnees-publique.medicaments.gouv.fr/extrait.php?specid='+$routeParams.id;
	}
]);