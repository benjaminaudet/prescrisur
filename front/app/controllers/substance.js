angular.module('prescrisurApp.controllers')

.controller("SubstanceController", [
	'$scope',
	'$state',
	'$stateParams',
	'$timeout',
	'Flash',
	'PageTitleService',
	'SubstanceService',
	'PathologySubstanceService',

	function($scope, $state, $stateParams, $timeout, Flash, PageTitleService, SubstanceService, PathologySubstanceService) {
		$scope.substance = null;
		$scope.pathologies = [];

		SubstanceService.get({ id: $stateParams.id }, function(data) {
			$scope.substance = data.data;
			PageTitleService.setTitle($scope.substance.name + ' | Substance');
		}, function() {
			Flash.create('danger', "Cette Substance n'existe pas ! Redirection...", 1500);
			$timeout(function() {
				$state.go('home');
			}, 1500);
		});

		PathologySubstanceService.get({ id: $stateParams.id }, function(data) {
			$scope.pathologies = data.data;
		})
	}
]);
