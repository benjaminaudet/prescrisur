angular.module('prescrisurApp.commonsServices', ['ngResource'])

.factory('MailService', ['$resource',
	function($resource){
		return $resource('/api/mail', null, {
			send: { method: 'POST' }
		});
	}
]);