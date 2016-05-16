angular.module('prescrisurApp.controllers')

.controller("SubstanceController", [
	'$scope',
	'$stateParams',
	'PageTitleService',
	'SubstanceService',
	'PathologySubstanceService',

	function($scope, $stateParams, PageTitleService, SubstanceService, PathologySubstanceService) {
		$scope.substance = null;
		$scope.pathologies = [];

		SubstanceService.get({ id: $stateParams.id }, function(data) {
			$scope.substance = data.data;
			PageTitleService.setTitle($scope.substance.name + ' | Substance');
		});

		PathologySubstanceService.get({ id: $stateParams.id }, function(data) {
			$scope.pathologies = data.data;
		})
	}
]);
