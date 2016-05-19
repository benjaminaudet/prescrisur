angular.module('prescrisurApp.controllers')

.controller("PageController", [
	'$scope',
	'$window',
	'$timeout',
	'$stateParams',
	'PageTitleService',
	'PageService',

	function($scope, $window, $timeout, $stateParams, PageTitleService, PageService) {
		$scope.page = null;

		if ($stateParams.id) {
			PageService.get({ id: $stateParams.id }, function(data) {
				$scope.page = data.data;
				PageTitleService.setTitle($scope.page.name);
			});
		} else {
			PageService.get(function(data) {
				$scope.pages = data.data;
				PageTitleService.setTitle('Administration des Pages');
			});
		}

		$scope.print = function() {
			showAllTexts(true);
			$timeout(function() {
				onPrintFinished($window.print());
			}, 100);
		};

		var showAllTexts = function(value) {
			$scope.pages.forEach(function(p) {
				p.showText = value;
			});
		};

		var onPrintFinished = function(printed) {
			showAllTexts(false);
		}
	}
])

.controller("PageEditController", [
	'$scope',
	'$state',
	'$stateParams',
	'PageTitleService',
	'ConfirmQuitService',
	'PageService',

	function($scope, $state, $stateParams, PageTitleService, ConfirmQuitService, PageService) {
		PageTitleService.setTitle('Nouvelle Page');
		ConfirmQuitService.init($scope);

		if($stateParams.id) {
			PageService.get({ id: $stateParams.id }, function(data) {
				$scope.page = data.data;
				PageTitleService.setTitle('Modifier une Page');
			});
		}

		$scope.submit = function () {
			var afterSave = function (data) {
				var savedPage = data.data;
				$state.go('pages.read', {id: savedPage._id});
			};
			var afterError = function() {
				ConfirmQuitService.init($scope);
			};

			if(confirm('Enregistrer les modifications ?')) {
				ConfirmQuitService.destroy();
				if ($stateParams.id) {
					PageService.update({id: $stateParams.id}, $scope.page, afterSave, afterError);
				} else {
					PageService.save($scope.page, afterSave, afterError);
				}
			}
			//console.log($scope.page);
		};
	}
]);