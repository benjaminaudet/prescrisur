angular.module('prescrisurApp.filters', [])

.filter('gradify', ['$state', '$sce',
	function($state, $sce) {
		return function(input) {
			// Grade A/B/C + Accord d'experts
			var regxABC = /(Grade (?:A|B|C)|AE|Accords d'experts)/gi;
			var matches = regxABC.exec(input);

			var labels = {
				"Grade A": "preuve scientifique établie",
				"Grade B": "présomption scientifique",
				"Grade C": "faible niveau de preuve scientifique",
				"AE": "approbation, en l’absence de données scientifiques disponibles, d’au moins 80 % des membres du groupe de travail",
				"Accords d'experts": "approbation, en l’absence de données scientifiques disponibles, d’au moins 80 % des membres du groupe de travail"
			};
			var link = "pages.read({id: 'presentation'})";

			if (matches) {
				input = input.replace(regxABC, '<a uib-tooltip="'+labels[matches[1]]+'" class="grade" ui-sref="'+link+'">$1</a>');
			}

			// Grade X..
			var regxX = /(Grade X[a-z0-9]{2})/gi;
			input = input.replace(regxX, '<a class="grade">$1</a>');

			return $sce.trustAsHtml(input);
		};
	}
]);