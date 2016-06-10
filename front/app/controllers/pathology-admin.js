angular.module('prescrisurApp.controllers')

.controller("PathologyAdminController", [
	'$scope',
	'PathologyService',
	'PathologyDraftService',

	function($scope, PathologyService, PathologyDraftService) {
		PathologyDraftService.get(function(data) {
			$scope.drafts = data.data;
		});

		PathologyService.get(function(data) {
			$scope.pathologies = data.data;
		});
	}
]);