angular.module('prescrisurApp.filters', [])

.filter('gradify', ['$state',
	function($state) {
		return function(input) {
			var regx = /(Grade (?:A|B|C|X[a-z0-9]{2}))/gi;
			return input.replace(regx, '<a class="grade" href="#/pages/presentation">$1</a>');
		};
	}
]);