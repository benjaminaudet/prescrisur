angular.module('prescrisurApp.commonsServices', ['ngResource'])

.factory('MailService', ['$resource',
	function($resource){
		return $resource('/api/mail', null, {
			send: { method: 'POST' }
		});
	}
])

.factory('PageTitleService', function() {
	var title = 'Prescrisur';
	return {
		title: function() { return title; },
		setTitle: function(newTitle) { title = newTitle }
	};
});