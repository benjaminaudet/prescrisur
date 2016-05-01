angular.module('prescrisurApp.controllers')

.controller("PageController", [
	'$scope',
	'$stateParams',
	'NewsService',

	function($scope, $stateParams, NewsService) {
		$scope.page = null;

		PageService.get({ id: $stateParams.id }, function(data) {
			$scope.page = data.data;
		});
	}
])

.controller("PageEditController", [
	'$scope',
	'$location',
	'$stateParams',
	'NewsService',

	function($scope, $location, $stateParams, NewsService) {

		if($stateParams.id) {
			PageService.get({ id: $stateParams.id }, function(data) {
				$scope.page = data.data;
			});
		}

		$scope.submit = function () {
			var afterSave = function (data) {
				var savedPage = data.data;
				$location.path('/pages/' + savedPage._id);
			};

			if ($stateParams.id) {
				PageService.update({id: $stateParams.id}, $scope.page, afterSave);
			} else {
				PageService.save($scope.page, afterSave);
			}
			//console.log($scope.page);
		};
	}
]);