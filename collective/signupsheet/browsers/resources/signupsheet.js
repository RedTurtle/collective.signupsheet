/**
 * Script for collective.signupshet
 */

(function($) {
	$(document).ready(function() {

		var allRegistrants = [];
		$('.availableRegistrants :checkbox').each(function() {
			allRegistrants.push($(this).val());
		});
		var confirmedRegistrants = [];
		$('.availableRegistrants :checkbox[data-state=confirmed]').each(function() {
			confirmedRegistrants.push($(this).val());
		});
		var unconfirmedRegistrants = [];
		$('.availableRegistrants :checkbox[data-state=unconfirmed]').each(function() {
			unconfirmedRegistrants.push($(this).val());
		});
		var waitinglistRegistrants = [];
		$('.availableRegistrants :checkbox[data-state= waiting_list_unconfirmed]').each(function() {
			waitinglistRegistrants.push($(this).val());
		});

		function NotifyRegistrantsViewModel() {
			var self = this;
		    this.toBeNotified = ko.observableArray(allRegistrants.slice(0));

			this.allNoneSelected = ko.observable(true);
			this.selectAllNone = function() {
				self.confirmedSelected(false);
				self.unconfirmedSelected(false);
				self.waitinglistSelected(false);				
				if (self.allNoneSelected()) {
					self.toBeNotified.removeAll();
				} else {
					self.toBeNotified(allRegistrants.slice(0));
				}
				return true;
			};

			this.confirmedSelected = ko.observable(false);			
			this.selectConfirmed = function() {
				self.allNoneSelected(false);
				self.unconfirmedSelected(false);
				self.waitinglistSelected(false);				
				if (self.confirmedSelected()) {
					self.toBeNotified.removeAll(confirmedRegistrants.slice(0));
				} else {
					self.toBeNotified(confirmedRegistrants.slice(0));
				}
				return true;				
			}

			this.unconfirmedSelected = ko.observable(false);			
			this.selectUnconfirmed = function() {
				self.allNoneSelected(false);
				self.confirmedSelected(false);
				self.waitinglistSelected(false);				
				if (self.unconfirmedSelected()) {
					self.toBeNotified.removeAll(unconfirmedRegistrants.slice(0));
				} else {
					self.toBeNotified(unconfirmedRegistrants.slice(0));
				}
				return true;				
			}

			this.waitinglistSelected = ko.observable(false);			
			this.selectWaitinglist = function() {
				self.allNoneSelected(false);
				self.confirmedSelected(false);
				self.unconfirmedSelected(false);				
				if (self.waitinglistSelected()) {
					self.toBeNotified.removeAll(waitinglistRegistrants.slice(0));
				} else {
					self.toBeNotified(waitinglistRegistrants.slice(0));
				}
				return true;				
			}

		};

		ko.applyBindings(new NotifyRegistrantsViewModel());

	});
})(jQuery);
