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
	'$state',
	'$stateParams',
	'PageTitleService',
	'ConfirmQuitService',
	'NewsService',

	function($scope, $state, $stateParams, PageTitleService, ConfirmQuitService, NewsService) {
		PageTitleService.setTitle('Nouvelle News');
		ConfirmQuitService.init($scope);

		if($stateParams.id) {
			NewsService.get({ id: $stateParams.id }, function(data) {
				$scope.news = data.data;
				PageTitleService.setTitle('Modifier une News');
			});
		}

		$scope.submit = function () {
			var afterSave = function (data) {
				var savedPage = data.data;
				$state.go('news.read', { id: savedPage._id });
			};
			var afterError = function() {
				ConfirmQuitService.init($scope);
			};

			if(confirm('Enregistrer les modifications ?')) {
				ConfirmQuitService.destroy();
				if ($stateParams.id) {
					NewsService.update({id: $stateParams.id}, $scope.news, afterSave, afterError);
				} else {
					NewsService.save($scope.news, afterSave, afterError);
				}
			}
			//console.log($scope.news);
		};
	}
]);