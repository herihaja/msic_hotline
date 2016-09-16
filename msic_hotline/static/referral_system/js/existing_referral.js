		// Automatic calculation of expiry date
    function autoSetExpiryDate(){
    	 var nowTemp = new Date();
    	 var now = new Date(nowTemp.getFullYear(), nowTemp.getMonth(), nowTemp.getDate(), 0, 0, 0, 0);
    	 var checkin = $('#referral-date').fdatepicker({
    		 format: 'yyyy-mm-dd',
    		 weekStart: 1,
    	 	 onRender: function (date) {
    	 		// return date.valueOf() < now.valueOf() ? 'disabled' : '';
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
    	 
    	
    }
	
	function selectFacility(){
		_quest_20 = $("#selected_facility").val();
		$.ajax({
		    url: '/referral_system/ajaxSelectFacility/',
		    data: { quest_20 : _quest_20 },
		    type: 'post', // This is the default though, you don't actually need to always mention it
		    success: function(data) {
		    	
		    	data = data.split('====');
		    	
		    	var _html = "<div class='callout success'>";
		    	_html += "<span class='round label warning'><h6>" + data[12] + "<br>" + data[0] + "</h6></span><hr />";
		    	
		    	_html += "<h6>Address [KHMER]</h6>";
		    	_html += "<p>" + data[13] + " ";
		    	_html += "" + data[14] + " ";
		    	_html += "" + data[15] + " ";
		    	_html += "" + data[16] + " ";
		    	_html += "" + data[17] + "</p> ";
		    	
		    	_html += "<h6>Address [EN]</h6>";
		    	_html += "<p>" + data[2] + " ";
		    	_html += "" + data[3] + " ";
		    	_html += "" + data[4] + " ";
		    	_html += "" + data[5] + " ";
		    	_html += "" + data[6] + "</p> ";		    			    
		    	
		    	_html += "<h6>Contact Telephone</h6>";
		    	_html += "<p>" + data[7] + "</p>";
		    	_html += "<h6>Opening Hours</h6>";
		    	_html += "<p>" + data[8] + "</p>";
		    	_html += "<h6>Available Services</h6>";
		    	_html += "<p><b>Referred Services: </b>" + textToBulletList(data[18]) + "</p>";
		    	_html += "</div>";
				
		    	//$("#id_selected_facility").val(_quest_21);
				$("#selected-facility-div").html(_html);
		    },
		    failure: function(data) { 
		        alert('Got an error dude');
		    }
		}); 
	}