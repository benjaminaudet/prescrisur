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
		$scope.editMode = false;

		$scope.msg = $stateParams.msg;

		AssociationService.get(function(data) {
			$scope.associations = data.data;
		});

		$scope.delete = function(assoID) {
			AssociationService.delete({id: assoID}, function(data) {
				if (data.success) {
					$state.go('associations', {msg: 'Association Supprimée !'}, {reload: true})
				}
			});
		};

		$scope.edit = function(asso) {
			$scope.editMode = true;
			$scope.association = asso;
		};
		
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
			var afterSave = function (msg) {
				return function() {
					$state.go('associations', {msg: msg}, {reload: true})
				}
			};
			if($scope.editMode) {
				AssociationService.update({ id: $scope.association._id }, $scope.association, afterSave('Association Modifiée !'));
			} else {
				AssociationService.save($scope.association, afterSave('Association Créée !'));
			}
			// console.log($scope.association);
		};
		
		$scope.cancel = function () {
			$scope.association = emptyAssociation;
			$scope.editMode = false;
		};


		var searchMessage = function(msg) {
			return [{
				_id: null,
				name: msg
			}];
		};
	}
]);
