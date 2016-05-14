angular.module('prescrisurApp.controllers')

.controller("SubstanceController", [
	'$scope',
	'$stateParams',
	'PageTitleService',
	'SubstanceService',
	'SubstancePathologyService',

	function($scope, $stateParams, PageTitleService, SubstanceService, SubstancePathologyService) {
		$scope.substance = null;
		$scope.pathologies = [];

		SubstanceService.get({ id: $stateParams.id }, function(data) {
			$scope.substance = data.data;
			PageTitleService.setTitle($scope.substance.name + ' | Substance');
		});

		SubstancePathologyService.get({ id: $stateParams.id }, function(data) {
			$scope.pathologies = data.data;
		})
	}
]);
