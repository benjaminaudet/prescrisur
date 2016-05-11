angular.module('prescrisurApp.controllers')

.controller("ContactController", [
	'$scope',
	'MailService',

	function($scope, MailService) {
		$scope.contactForm = {};
		
		if($scope.currentUser) {
			$scope.contactForm.sender = {name: $scope.currentUser.name, email: $scope.currentUser._id};
		}

		$scope.submit = function() {
			MailService.send($scope.contactForm, function(data) {
				$scope.msg = 'Message Envoyé !';
			});
			// console.log($scope.contactForm);
		}
	}
]);