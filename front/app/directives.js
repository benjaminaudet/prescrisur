angular.module('prescrisurApp.directives', [])

.directive('levelTitle', function () {
	return {
		restrict: 'E',
		templateUrl: 'partials/level-title.html',
		scope: {
			depth: '@',
			rank: '@',
			title: '@'
		}
	};
});