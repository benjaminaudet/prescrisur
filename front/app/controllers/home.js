angular.module('prescrisurApp.controllers')

.controller("HomeController", [
	'$scope',
	'SearchService',

	function($scope, SearchService) {
		$scope.q = null;
		$scope.results = [];

		$scope.search = function() {
			if($scope.q.length > 0) {
				SearchService.get({q: $scope.q}, function(data) {
					$scope.results = data.data;
				});
			} else {
				$scope.results = [];
			}
		};
	}
]);
