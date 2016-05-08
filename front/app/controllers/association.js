angular.module('prescrisurApp.controllers')

.controller("AssociationController", [
	'$scope',
	'$state',
	'$stateParams',
	'AssociationService',
	'SearchService',

	function($scope, $state, $stateParams, AssociationService, SearchService) {
		var emptyAssociation = {name: null, substances: []};
		$scope.association = emptyAssociation;

		$scope.msg = $stateParams.msg;

		$scope.search = function($select) {
			var search = '';
			if($select) {
				search = $select.search;
			}
			$scope.results = searchMessage('Recherche en cours...');
			SearchService.get({q: search, searchType: 'substances'}, function(data) {
				$scope.results = data.data;
				if ($scope.results.length == 0) {
					$scope.results = searchMessage('Aucun résultat');
				}
			});
		};

		$scope.addSubstance = function($select) {
			if($scope.association.substances.indexOf($select.selected) == -1) {
				return $scope.association.substances.push($select.selected);
			}
		};
		
		$scope.removeSubstance = function($index) {
			$scope.association.substances.splice($index, 1);
		};

		$scope.submit = function () {
			var afterSave = function () {
				$state.go('associations', {msg: 'Association Créée !'}, {reload: true})
			};
			AssociationService.save($scope.association, afterSave);
			// console.log($scope.association);
		};
		
		$scope.cancel = function () {
			$scope.association = emptyAssociation;
		};


		var searchMessage = function(msg) {
			return [{
				_id: null,
				name: msg
			}];
		};
	}
]);
