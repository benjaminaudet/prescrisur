angular.module('prescrisurApp.controllers')

.controller("PathologyController", [
	'$scope',
	'$routeParams',
	'PathologyService',

	function($scope, $routeParams, PathologyService) {
		$scope.pathology = null;

		PathologyService.get({ id: $routeParams.id }, function(data) {
			$scope.pathology = data.data;
		});
	}
])

.controller("PathologyEditController", [
	'$scope',
	'$location',
	'$routeParams',
	'PathologyService',

	function($scope, $location, $routeParams, PathologyService) {

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
			data.levels.push({rank: rank, depth: depth, levels: []});
		};

		$scope.addRoot = function() {
			$scope.pathology.levels.push({rank: '', depth: 1, levels:[]});
		};

		$scope.submit = function() {
			var afterSave = function(data) {
				var savedPatho = data.data;
				$location.path('/pathologies/'+savedPatho._id);
			};

			if($routeParams.id) {
				PathologyService.update({ id: $routeParams.id }, $scope.pathology, afterSave);
			} else {
				PathologyService.save($scope.pathology, afterSave);
			}
		};

		var getPathology = function() {
			if($routeParams.id) {
				PathologyService.get({ id: $routeParams.id }, function(data) {
					$scope.pathology = data.data;
				});
			}
			else {
				$scope.pathology = {
					name: null,
					levels: [
						{rank: '', depth: 1, levels: []}
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