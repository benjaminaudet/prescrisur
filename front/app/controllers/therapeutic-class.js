angular.module('prescrisurApp.controllers')

	.controller("TherapeuticClassController", [
		'$scope',
		'$state',
		'$stateParams',
		'Flash',
		'PageTitleService',
		'TherapeuticClassService',

		function($scope, $state, $stateParams, Flash, PageTitleService, TherapeuticClassService) {
			$scope.therapeuticClass = null;
			
			TherapeuticClassService.get({id: $stateParams.id}, function(data) {
				$scope.therapeuticClass = data.data;
				PageTitleService.setTitle($scope.therapeuticClass.name + '| Classe Pharmaco-Thérapeutique');
			});

			$scope.delete = function() {
				if(confirm('Voulez-vous supprimer cette Classe ?')) {
					TherapeuticClassService.delete({ id: $stateParams.id }, function(data) {
						Flash.create('success', 'Classe Supprimée !');
						$state.go('home');
					});
				}
			};

			$scope.entryColspan = function(entry) {
				if(entry.info) {
					return 1;
				}
				return 2;
			};
		}
	]);
