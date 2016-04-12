angular.module('prescrisurApp.controllers')

.controller("HomeController", [
	'$scope',
	'SearchService',

	function($scope, SearchService) {
		$scope.q = null;
		$scope.searchType = 'specialities';
		$scope.results = [];

		$scope.search = function() {
			if($scope.q.length > 1) {
				SearchService.get({q: $scope.q, searchType: $scope.searchType}, function(data) {
					$scope.results = data.data;
				});
			} else {
				$scope.results = [];
			}
		};
	}
]);
