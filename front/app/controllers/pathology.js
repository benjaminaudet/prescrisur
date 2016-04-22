angular.module('prescrisurApp.controllers')

.controller("PathologyController", [
	'$scope',
	'$stateParams',
	'PathologyService',

	function($scope, $stateParams, PathologyService) {
		$scope.pathology = null;

		PathologyService.get({ id: $stateParams.id }, function(data) {
			$scope.pathology = data.data;
		});
	}
])

.controller("PathologyEditController", [
	'$scope',
	'$location',
	'$stateParams',
	'PathologyService',

	function($scope, $location, $stateParams, PathologyService) {

		$scope.delete = function(data, $index) {
			var levelName = getRank(data.rank, $index);
			var splitLevel = levelName.split('.');
			splitLevel = splitLevel.slice(0, -1);
			var toDel = splitLevel.pop() - 1;
			var levelToGo = $scope.pathology.levels;
			splitLevel.forEach(function(i) {
				levelToGo = levelToGo[i-1].levels;
			});
			levelToGo.splice(toDel, 1);
		};

		$scope.add = function(data, $index) {
			var rank = getRank(data.rank, $index);
			var depth = data.depth + 1;
			if(!data.levels) {
				data.levels = [];
			}
			data.levels.push({rank: rank, depth: depth});
		};

		$scope.addRoot = function() {
			$scope.pathology.levels.push({rank: '', depth: 1});
		};

		$scope.submit = function() {
			var afterSave = function(data) {
				var savedPatho = data.data;
				$location.path('/pathologies/'+savedPatho._id);
			};

			//if($stateParams.id) {
			//	PathologyService.update({ id: $stateParams.id }, $scope.pathology, afterSave);
			//} else {
			//	PathologyService.save($scope.pathology, afterSave);
			//}
			console.log($scope.pathology)
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

		getPathology();
	}
]);
