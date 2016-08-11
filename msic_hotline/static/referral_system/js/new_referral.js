	// Automatic calculation of expiry date
    function autoSetExpiryDate(){
    	 var nowTemp = new Date();
    	 var now = new Date(nowTemp.getFullYear(), nowTemp.getMonth(), nowTemp.getDate(), 0, 0, 0, 0);
    	 var checkin = $('#referral-date').fdatepicker({
    		 format: 'yyyy-mm-dd',
    		 weekStart: 1,
    	 	 onRender: function (date) {
    	 		return date.valueOf() < now.valueOf() ? 'disabled' : '';
    	 	 }
    	 }).on('changeDate', function (ev) {
    	 	if (ev.date.valueOf() > checkout.date.valueOf()) {
    	 		
    	 	}
    	 	var newDate = new Date(ev.date)
	 		newDate.setDate(newDate.getDate() + 30);
	 		checkout.update(newDate);
	 		
    	 	checkin.hide();
    	 	$('#expiry-date')[0].focus();
    	 }).data('datepicker');
    	 
    	 var checkout = $('#expiry-date').fdatepicker({
    		format: 'yyyy-mm-dd',
    		weekStart: 1,
    	 	onRender: function (date) {
    	 		return date.valueOf() <= checkin.date.valueOf() ? 'disabled' : '';
    	 	}
    	 }).on('changeDate', function (ev) {
    	 	checkout.hide();
    	 }).data('datepicker');
    	 
    	 
    	 //default date now and now + 30
    	 checkin.update(now);
    	 var newDate = new Date();
    	 newDate.setDate(newDate.getDate() + 30);
 		 checkout.update(newDate);
    	
    }