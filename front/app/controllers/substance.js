angular.module('prescrisurApp.controllers')

.controller("SubstanceController", [
	'$scope',
	'$routeParams',
	'SubstanceService',

	function($scope, $routeParams, SubstanceService) {
		$scope.substance = null;

		SubstanceService.get({ id: $routeParams.id }, function(data) {
			$scope.substance = data.data;
		});
	}
]);
