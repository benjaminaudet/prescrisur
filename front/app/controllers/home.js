angular.module('prescrisurApp.controllers')

.controller("HomeController", [
	'$scope',
	'$state',
	'$stateParams',
	'PageTitleService',
	'SearchService',
	'NewsService',
	'PathologyService',

	function($scope, $state, $stateParams, PageTitleService, SearchService, NewsService, PathologyService) {
		PageTitleService.setTitle("Outil d'aide à la Prescription");

		$scope.q = null;
		$scope.searchType = 'pathologies';
		$scope.results = [];
		
		NewsService.get(function(data) {
			$scope.news = data.data;
		});
		
		PathologyService.get(function(data) {
			$scope.pathologies = data.data;
		});
		
		$scope.goTo = function($select) {
			var searchType = $scope.searchType;
			if(searchType == 'pathologies') {
				searchType += '.read';
			}
			$state.go(searchType, {id: $select.selected._id});
		};

		$scope.search = function($select) {
			var search = '';
			if($select) {
				search = $select.search;
			}
			$scope.results = searchMessage('Recherche en cours...');
			SearchService.get({q: search, searchType: $scope.searchType}, function(data) {
				$scope.results = data.data;
				if ($scope.results.length == 0) {
					$scope.results = searchMessage('Aucun résultat');
				}
			});
		};

		$scope.$watch('searchType', function(newValue, oldValue) {
			if(newValue == oldValue) { return; }
			$scope.results = [];
			$scope.search();
		});

		var searchMessage = function(msg) {
			return [{
				_id: null,
				name: msg
			}];
		};
	}
]);