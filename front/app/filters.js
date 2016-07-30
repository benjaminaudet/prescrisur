angular.module('prescrisurApp.filters', [])

.filter('gradify', ['$state', '$sce',
	function($state, $sce) {
		return function(input) {
			// Grade A/B/C + Accord d'experts
			var regxABC = /(Grade (?:A|B|C|D)|(?:\s|\()AE|Accords d'experts)/gi;
			var matches = regxABC.exec(input);

			var labels = {
				"grade a": "preuve scientifique établie",
				"grade b": "présomption scientifique",
				"grade c": "faible niveau de preuve scientifique",
				"ae": "approbation, en l’absence de données scientifiques disponibles, d’au moins 80 % des membres du groupe de travail",
				"accords d'experts": "approbation, en l’absence de données scientifiques disponibles, d’au moins 80 % des membres du groupe de travail"
			};

			if (matches) {
				var tooltip = labels[matches[1].toLowerCase()];
				var link = "pages.read({id: 'presentation'})";
				input = input.replace(regxABC, '<a uib-tooltip="'+tooltip+'" class="grade" ui-sref="'+link+'">$1</a>');
			}

			// Grade D/X..
			var regxX = /(Grade (?:D|X[a-z0-9]{2}))/gi;
			input = input.replace(regxX, '<a class="grade">$1</a>');

			return $sce.trustAsHtml(input);
		};
	}
]);