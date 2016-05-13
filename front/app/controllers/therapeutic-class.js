angular.module('prescrisurApp.controllers')

	.controller("TherapeuticClassController", [
		'$scope',
		'$stateParams',
		'TherapeuticClassService',

		function($scope, $stateParams, TherapeuticClassService) {
			$scope.therapeuticClass = null;
			
			TherapeuticClassService.get({id: $stateParams.id}, function(data) {
				$scope.therapeuticClass = data.data;
			})
		}
	]);
