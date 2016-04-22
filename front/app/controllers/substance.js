angular.module('prescrisurApp.controllers')

.controller("SubstanceController", [
	'$scope',
	'$stateParams',
	'SubstanceService',

	function($scope, $stateParams, SubstanceService) {
		$scope.substance = null;

		SubstanceService.get({ id: $stateParams.id }, function(data) {
			$scope.substance = data.data;
		});
	}
]);
