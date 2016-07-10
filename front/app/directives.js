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
})

.directive("ngBindHtmlCompile", function($compile, $sce){
	return {
		restrict: "A",
		link: function(scope, element, attrs){
			scope.$watch($sce.parseAsHtml(attrs.ngBindHtmlCompile), function(html){
				var el = angular.element("<div>").html(html);
				element.empty();
				element.append(el.children());
				$compile(element.contents())(scope);
			})
		}
	};
});