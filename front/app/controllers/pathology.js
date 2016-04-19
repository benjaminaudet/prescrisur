angular.module('prescrisurApp.controllers')

.controller("PathologyController", [
	'$scope',

	function($scope) {
		var getLevelName = function(parentLevelName, $index) {
			return parentLevelName + ($index + 1) + '.';
		};

		$scope.delete = function(data, $index) {
			var levelName = getLevelName(data.parentLevelName, $index);
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
			var levelName = getLevelName(data.parentLevelName, $index);
			var depth = data.depth + 1;
			data.levels.push({parentLevelName: levelName, depth: depth, levels: []});
		};

		$scope.addRoot = function() {
			$scope.pathology.levels.push({parentLevelName: '', depth: 1, levels:[]});
		};

		$scope.submit = function() {
			console.log($scope.pathology);
		};

		$scope.pathology = {
			name: null,
			levels: [
				{parentLevelName: '', depth: 1, levels: []}
			]
		};
	}
]);
