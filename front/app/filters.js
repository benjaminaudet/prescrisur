angular.module('prescrisurApp.filters', [])

.filter('gradify', ['$state',
	function($state) {
		return function(input) {
			// Grade A/B/C + Accord d'experts
			var regxABC = /(Grade (?:A|B|C)|AE|Accords d'experts)/gi;
			input = input.replace(regxABC, '<a class="grade" href="#/pages/presentation">$1</a>');

			// Grade X..
			var regxX = /(Grade X[a-z0-9]{2})/gi;
			input = input.replace(regxX, '<a class="grade">$1</a>');

			return input;
		};
	}
]);