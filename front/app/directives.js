angular.module('prescrisurApp.directives', [])

.directive('levelTitle', function () {
	return {
		restrict: 'E',
		templateUrl: 'front/app/templates/partials/level-title.html',
		scope: {
			depth: '@',
			rank: '@',
			title: '@'
		}
	};
});