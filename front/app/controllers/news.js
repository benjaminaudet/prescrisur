angular.module('prescrisurApp.controllers')

.controller("NewsController", [
	'$scope',
	'$state',
	'$stateParams',
	'PageTitleService',
	'NewsService',

	function($scope, $state, $stateParams, PageTitleService, NewsService) {

		if ($stateParams.id) {
			NewsService.get({ id: $stateParams.id }, function(data) {
				$scope.news = data.data;
				PageTitleService.setTitle($scope.news.name + ' | PrescriNews');
			});
		} else {
			NewsService.get(function(data){
				$scope.news = data.data;
				PageTitleService.setTitle('PrescriNews');
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
	'PageTitleService',
	'NewsService',

	function($scope, $location, $stateParams, PageTitleService, NewsService) {
		PageTitleService.setTitle('Nouvelle News');

		if($stateParams.id) {
			NewsService.get({ id: $stateParams.id }, function(data) {
				$scope.news = data.data;
				PageTitleService.setTitle('Modifier une News');
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