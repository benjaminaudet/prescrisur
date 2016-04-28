angular.module('prescrisurApp.controllers')

.controller("SubstanceController", [
	'$scope',
	'$stateParams',
	'SubstanceService',
	'SubstancePathologyService',

	function($scope, $stateParams, SubstanceService, SubstancePathologyService) {
		$scope.substance = null;
		$scope.pathologies = [];

		SubstanceService.get({ id: $stateParams.id }, function(data) {
			$scope.substance = data.data;
		});

		SubstancePathologyService.get({ id: $stateParams.id }, function(data) {
			$scope.pathologies = data.data;
		})
	}
]);
