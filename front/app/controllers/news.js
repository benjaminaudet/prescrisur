angular.module('prescrisurApp.controllers')

.controller("NewsController", [
	'$scope',
	'$state',
	'$stateParams',
	'NewsService',

	function($scope, $state, $stateParams, NewsService) {

		if ($stateParams.id) {
			NewsService.get({ id: $stateParams.id }, function(data) {
				$scope.news = data.data;
			});
		} else {
			NewsService.get(function(data){
				$scope.news = data.data;
			})
		}

		$scope.delete = function(news_id) {
			NewsService.delete({ id: news_id }, function() {
				$state.go('news', {msg: 'News Supprimée !'});
			});
		}
	}
])

.controller("NewsEditController", [
	'$scope',
	'$location',
	'$stateParams',
	'NewsService',

	function($scope, $location, $stateParams, NewsService) {

		if($stateParams.id) {
			NewsService.get({ id: $stateParams.id }, function(data) {
				$scope.news = data.data;
			});
		}

		$scope.submit = function () {
			var afterSave = function (data) {
				var savedPage = data.data;
				$location.path('/news/' + savedPage._id);
			};

			if ($stateParams.id) {
				NewsService.update({id: $stateParams.id}, $scope.news, afterSave);
			} else {
				NewsService.save($scope.news, afterSave);
			}
			//console.log($scope.news);
		};
	}
]);