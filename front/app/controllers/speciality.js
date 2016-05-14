angular.module('prescrisurApp.controllers')

.controller("SpecialityController", [
	'$scope',
	'$window',
	'$stateParams',
	'PageTitleService',

	function($scope, $window, $stateParams, PageTitleService) {
		PageTitleService.setTitle('Fiche du Médicament');

		$window.location.replace('http://base-donnees-publique.medicaments.gouv.fr/extrait.php?specid='+$stateParams.id);
	}
]);