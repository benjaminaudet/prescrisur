angular.module('prescrisurApp.controllers')

.controller("ContactController", [
	'$scope',
	'PageTitleService',
	'PageService',
	'MailService',

	function($scope, PageTitleService, PageService, MailService) {
		PageTitleService.setTitle('Aide à la Prescription');

		$scope.contactForm = {};
		
		if($scope.currentUser) {
			$scope.contactForm.sender = {name: $scope.currentUser.name, email: $scope.currentUser._id};
		}
		
		// Load texts
		PageService.get({id: 'contact-presentation-prescrisur'}, function(data) {
			$scope.textPrescrisur = data.data;
		});
		PageService.get({id: 'contact-presentation-nicole'}, function(data) {
			$scope.textNicole = data.data;
		});

		$scope.submit = function() {
			MailService.send($scope.contactForm, function(data) {
				$scope.msg = 'Message Envoyé !';
			});
			// console.log($scope.contactForm);
		}
	}
]);