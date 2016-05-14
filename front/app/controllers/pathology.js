angular.module('prescrisurApp.controllers')

.controller("PathologyController", [
	'$scope',
	'$state',
	'$window',
	'$timeout',
	'$location',
	'$stateParams',
	'PageTitleService',
	'PathologyService',

	function($scope, $state, $window, $timeout, $location, $stateParams, PageTitleService, PathologyService) {
		$scope.pathology = null;

		PathologyService.get({ id: $stateParams.id }, function(data) {
			$scope.pathology = data.data;
			PageTitleService.setTitle('Traitement de ' + $scope.pathology.name);
		});

		$scope.delete = function() {
			PathologyService.delete({ id: $stateParams.id }, function(data) {
				$state.go('home', {msg: 'Pathologie Supprimée !'});
			});
		};

		$scope.scrollTo = function(rank, $index) {
			var hashToGo = rank+($index+1)+'.';
			$location.hash(hashToGo);
		};

		$scope.entryColspan = function(entry) {
			if(entry.info) {
				return 1;
			}
			return 2;
		};

		$scope.print = function() {
			showAll($scope.pathology, true);
			$timeout(function() {
				onPrintFinished($window.print())
			}, 500);
		};

		var showAll = function(obj, value) {
			if(obj.hasOwnProperty('levels')) {
				obj.levels.forEach(function(l) {
					showAll(l, value);
				});
			} else if(obj.hasOwnProperty('entries')) {
				obj.entries.forEach(function(e) {
					if(e.hasOwnProperty('info')) {
						e.displayInfo = value;
					}
					if(e.product.hasOwnProperty('specialities')) {
						e.displaySpecialities = value;
					}
				});
			}
		};

		var onPrintFinished = function(printed) {
			showAll($scope.pathology, false);
		}
	}
])

.controller("PathologyEditController", [
	'$scope',
	'$location',
	'$stateParams',
	'PageTitleService',
	'SearchService',
	'PathologyService',

	function($scope, $location, $stateParams, PageTitleService, SearchService, PathologyService) {
		PageTitleService.setTitle('Nouvelle Pathologie');

		$scope.results = [];
		$scope.recommandations = ['none', 'alert', 'middle', 'ok'];
		$scope.productTypes = [
			{_id: 'specialities', name: 'Specialité'},
			{_id: 'substances', name: 'Substance'},
			{_id: 'associations', name: 'Association'}
		];

		if($stateParams.id) {
			PathologyService.get({ id: $stateParams.id }, function(data) {
				$scope.pathology = data.data;
				PageTitleService.setTitle('Modifier une Pathologie');
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


		$scope.filterResults = function(r) {
			var res = {name: r.name, _id: r._id, status: r.status};
			if(r.specialities) {
				res.specialities = r.specialities;
			}
			return res;
		};

		$scope.search = function($select, searchType, force) {
			var search = '';
			if($select) {
				search = $select.search;
			}

			var payload = {q: search, searchType: searchType};
			if (searchType == 'substances') {
				payload.specialities = true;
			}

			$scope.results = searchMessage('Recherche en cours...');
			if(force || search.length > 0) {
				SearchService.get(payload, function(data) {
					$scope.results = data.data;
					if ($scope.results.length == 0) {
						$scope.results = searchMessage('Aucun résultat');
					}
				});
			}
		};

		$scope.displaySpecialities = function(specialities) {
			if(!specialities[0].hasOwnProperty('enabled')) {
				$scope.checkAllSpecialities(specialities);
			}
		};

		$scope.checkAllSpecialities = function(specialities, checkValue) {
			checkValue = (checkValue != undefined) ? checkValue : true;
			specialities.forEach(function(spec) {
				spec.enabled = checkValue;
			});
		};
		
		$scope.checkChildren = function(level) {
			if(!level.hasOwnProperty('levels')) {
				return;
			}
			level.levels.forEach(function(l) {
				l.is_class = level.is_class;
				$scope.checkChildren(l);
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

		var getRank = function(parentRank, $index) {
			return parentRank + ($index + 1) + '.';
		};

		var searchMessage = function(msg) {
			return [{
				_id: null,
				name: msg
			}];
		};


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

		$scope.isSubstance = function(entry) {
			return entry.type == 'substances' && entry.hasOwnProperty('product') && entry.product._id && entry.product._id != '';
		};

		$scope.isSubstanceOrAsso = function(entry) {
			return (entry.type == 'substances' || entry.type == 'associations') && entry.hasOwnProperty('product') && entry.product._id && entry.product._id != '';
		};
	}
]);
