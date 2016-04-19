angular.module('prescrisurApp.controllers')

.controller("PathologyController", [
	'$scope',

	function($scope) {
		$scope.delete = function(data) {
			data.levels = [];
		};

		$scope.add = function(data) {
			var post = data.levels.length + 1;
			var levelName = data.levelName + post + '.';
			var depth = data.depth + 1;
			data.levels.push({levelName: levelName, depth: depth,levels: []});
		};

		$scope.addRoot = function(data) {
			var post = $scope.pathology.levels.length + 1;
			var levelName = post + '.';
			$scope.pathology.levels.push({levelName: levelName, depth: 1, levels:[]});
		};

		$scope.pathology = {
			name: null,
			levels: [
				{levelName: '1.', depth: 1, levels: []}
			]
		};
	}
]);
