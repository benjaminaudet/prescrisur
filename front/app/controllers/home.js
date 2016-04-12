angular.module('prescrisurApp.controllers')

.controller("HomeController", [
	'$scope',
	'Search',

	function($scope, Search) {
		$scope.q = null;
		$scope.results = [];

		$scope.search = function() {
			if($scope.q.length > 0) {
				Search.get({q: $scope.q}, function(data) {
					$scope.results = data.data;
				});
			} else {
				$scope.results = [];
			}
		};
	}
]);
