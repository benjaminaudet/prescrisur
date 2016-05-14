angular.module('prescrisurApp.controllers')

	.controller("TherapeuticClassController", [
		'$scope',
		'$stateParams',
		'PageTitleService',
		'TherapeuticClassService',

		function($scope, $stateParams, PageTitleService, TherapeuticClassService) {
			$scope.therapeuticClass = null;
			
			TherapeuticClassService.get({id: $stateParams.id}, function(data) {
				$scope.therapeuticClass = data.data;
				PageTitleService.setTitle($scope.therapeuticClass.name + '| Classe Pharmaco-Thérapeutique');
			})
		}
	]);
