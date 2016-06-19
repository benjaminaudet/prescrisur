angular.module('prescrisurApp.controllers')

.controller("PathologyController", [
	'$scope',
	'$state',
	'$window',
	'$timeout',
	'$location',
	'$stateParams',
	'Flash',
	'PageTitleService',
	'SearchService',
	'PathologyService',
	'PathologyDraftService',

	function($scope, $state, $window, $timeout, $location, $stateParams, Flash, PageTitleService, SearchService, PathologyService, PathologyDraftService) {
		$scope.pathology = null;
		$scope.foldAll = false;

		var pathoService = PathologyService;
		if($scope.isAuthorized('admin')) {
			if($stateParams.draft) {
				$scope.draftMode = true;
				pathoService = PathologyDraftService;
			} else {
				PathologyDraftService.hasDraft({ id: $stateParams.id }, function(data) {
					$scope.draftExists = data.exists;
				});
			}
		}
		
		pathoService.get({ id: $stateParams.id }, function(data) {
			$scope.pathology = data.data;
			PageTitleService.setTitle('Traitement de ' + $scope.pathology.name);
		}, function() {
			$scope.pathology = false;
			Flash.create('danger', "Cette Pathologie n'existe pas ! Redirection...");
			$timeout(function() {
				$state.go('home');
			}, 4000);
		});

		$scope.search = function($select) {
			var search = '';
			if($select) {
				search = $select.search;
			}
			$scope.results = searchMessage('Recherche en cours...');
			SearchService.get({q: search, searchType: 'pathologies'}, function(data) {
				$scope.results = data.data;
				if ($scope.results.length == 0) {
					$scope.results = searchMessage('Aucun résultat');
				}
			});
		};

		$scope.goTo = function($select) {
			$state.go('pathologies.read', {id: $select.selected._id});
		};

		$scope.validate = function() {
			if(confirm('Voulez-vous passer cette Pathologie en mode public ?')) {
				PathologyService.validate({ id: $stateParams.id }, function() {
					Flash.create('success', 'Pathologie validée !');
					$state.go('pathologies.read', { id: $stateParams.id, draft: null }, { reload: true });
				}, function() {
					Flash.create('danger', 'Un problème est survenu...');
				});
			}
		};

		$scope.unvalidate = function() {
			if(confirm('Voulez-vous invalider cette Pathologie ?')) {
				PathologyService.unvalidate({ id: $stateParams.id }, function() {
					Flash.create('success', 'Pathologie invalidée !');
					$state.go('pathologies.read', { id: $stateParams.id, draft: true }, { reload: true });
				}, function() {
					Flash.create('danger', 'Un problème est survenu...');
				});
			}
		};

		$scope.delete = function() {
			if(confirm('Voulez-vous supprimer cette Pathologie ?')) {
				PathologyService.delete({ id: $stateParams.id }, function(data) {
					Flash.create('success', 'Pathologie Supprimée !');
					$state.go('home');
				});
			}
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
			var onPrintFinished = function() {
				$scope.hide = false;
				showAll($scope.pathology, false);
			};

			$scope.hide = true;
			showAll($scope.pathology, true);
			$timeout(function() {
				onPrintFinished($window.print())
			}, 500);
		};

		$scope.toggleShowAll = function() {
			$scope.foldAll = !$scope.foldAll;
			showAll($scope.pathology, $scope.foldAll);
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

		var searchMessage = function(msg) {
			return [{
				_id: null,
				name: msg
			}];
		};
	}
]);