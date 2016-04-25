angular.module('prescrisurApp.controllers')

.controller("PathologyController", [
	'$scope',
	'$stateParams',
	'PathologyService',

	function($scope, $stateParams, PathologyService) {
		$scope.pathology = null;

		$scope.entryColspan = function(entry) {
			if(entry.info) {
				return 1;
			}
			return 2;
		};

		PathologyService.get({ id: $stateParams.id }, function(data) {
			$scope.pathology = data.data;
		});
	}
])

.controller("PathologyEditController", [
	'$scope',
	'$location',
	'$stateParams',
	'SearchService',
	'PathologyService',

	function($scope, $location, $stateParams, SearchService, PathologyService) {
		$scope.results = [];
		$scope.recommandations = ['none', 'alert', 'middle', 'ok'];
		$scope.productTypes = [
			{_id: 'specialities', 'name': 'Specialité'},
			{_id: 'substances', 'name': 'Substance'}
		];

		$scope.filterResults = function(r) {
			return {name: r.name, _id: r._id};
		};

		$scope.search = function($select, searchType) {
			var search = '';
			if($select) {
				search = $select.search;
			}
			$scope.results = searchMessage('Recherche en cours...');
			SearchService.get({q: search, searchType: searchType}, function(data) {
				$scope.results = data.data;
				if ($scope.results.length == 0) {
					$scope.results = searchMessage('Aucun résultat');
				}
			});
		};

		$scope.removeLevel= function(data, $index) {
			var levelName = getRank(data.rank, $index);
			var splitLevel = levelName.split('.');
			splitLevel = splitLevel.slice(0, -1);
			var toDel = splitLevel.pop() - 1;
			var levelToGo = $scope.pathology.levels;
			var supLevelToGo = $scope.pathology;
			splitLevel.forEach(function(i) {
				supLevelToGo = levelToGo[i-1];
				levelToGo = supLevelToGo.levels;
			});
			if(levelToGo.length == 1) {
				delete supLevelToGo.levels;
				return;
			}
			levelToGo.splice(toDel, 1);
		};

		$scope.removeEntry = function(level, $index) {
			if(level.entries.length == 1) {
				delete level.entries;
				return;
			}
			level.entries.splice($index, 1);
		};

		$scope.addSubLevel = function(data, $index) {
			var rank = getRank(data.rank, $index);
			var depth = data.depth + 1;
			if(data.entries) {
				delete data.entries;
			}
			if(!data.levels) {
				data.levels = [];
			}
			data.levels.push({rank: rank, depth: depth});
		};

		$scope.addEntry = function(data) {
			if(!data.entries) {
				data.entries = [];
			}
			data.entries.push({reco: {_id: 'none'}, type: 'specialities'});
		};

		$scope.addInfo = function(entry) {
			entry.info = 'Info';
		};

		$scope.addRootLevel = function() {
			$scope.pathology.levels.push({rank: '', depth: 1});
		};

		$scope.submit = function() {
			var afterSave = function(data) {
				var savedPatho = data.data;
				$location.path('/pathologies/'+savedPatho._id);
			};

			if($stateParams.id) {
				PathologyService.update({ id: $stateParams.id }, $scope.pathology, afterSave);
			} else {
				PathologyService.save($scope.pathology, afterSave);
			}
			//console.log($scope.pathology);
		};

		var getPathology = function() {
			if($stateParams.id) {
				PathologyService.get({ id: $stateParams.id }, function(data) {
					$scope.pathology = data.data;
				});
			}
			else {
				$scope.pathology = {
					name: null,
					levels: [
						{rank: '', depth: 1}
					]
				};
			}
		};

		var getRank = function(parentRank, $index) {
			return parentRank + ($index + 1) + '.';
		};

		var searchMessage = function(msg) {
			return [{
				_id: null,
				name: msg
			}];
		};

		getPathology();


		// Function to display or not action buttons
		$scope.canAddRootLevel = function(data, $index) {
			return data.depth == 1 && $index == 0;
		};

		$scope.canAddSubLevel = function(data) {
			return data.depth < 4;
		};

		$scope.canAddEntry = function(data) {
			return !data.levels || data.levels.length == 0;
		};

		$scope.canRemoveLevel = function(data) {
			if(data.depth == 1) {
				return $scope.pathology.levels.length > 1;
			}
			return !data.levels;
		};
	}
]);
