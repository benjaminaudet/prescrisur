angular.module('prescrisurApp.controllers')

.controller("SubstanceController", [
	'$scope',
	'$routeParams',
	'Substance',

	function($scope, $routeParams, Substance) {
		$scope.substance = null;

		Substance.get({ id: $routeParams.id }, function(data) {
			$scope.substance = data.data;
		});
	}
]);
