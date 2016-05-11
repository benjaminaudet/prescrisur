angular.module('prescrisurApp.controllers')

.controller("PageController", [
	'$scope',
	'$stateParams',
	'PageService',

	function($scope, $stateParams, PageService) {
		$scope.page = null;

		if ($stateParams.id) {
			PageService.get({ id: $stateParams.id }, function(data) {
				$scope.page = data.data;
			});
		} else {
			PageService.get(function(data) {
				$scope.pages = data.data;
			});
		}
		
	}
])

.controller("PageEditController", [
	'$scope',
	'$location',
	'$stateParams',
	'PageService',

	function($scope, $location, $stateParams, PageService) {

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