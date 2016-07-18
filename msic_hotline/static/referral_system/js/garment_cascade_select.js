	
    // Automatic calculation of expiry date
    function autoSetExpiryDate(){
    	 var nowTemp = new Date();
    	 var now = new Date(nowTemp.getFullYear(), nowTemp.getMonth(), nowTemp.getDate(), 0, 0, 0, 0);
    	 var checkin = $('#referral-date').fdatepicker({
    		 format: 'yyyy-mm-dd',
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
    	 	onRender: function (date) {
    	 		return date.valueOf() <= checkin.date.valueOf() ? 'disabled' : '';
    	 	}
    	 }).on('changeDate', function (ev) {
    	 	checkout.hide();
    	 }).data('datepicker');
    	
    }

	function loadGFDistrict(_province){
		$.ajax({
		    url: '/referral_system/ajaxListGFDistrict/',
		    data: { province : _province },
		    type: 'post', // This is the default though, you don't actually need to always mention it
		    success: function(data) {
		    	dataJson = $.parseJSON(data);
		    	var _html = "<option value='0'>-- Select --</option>";
				$.each(dataJson, function(index) {
					_html += "<option onclick=\"loadGFVillage('" + dataJson[index].district + "')\" value='" + dataJson[index].district + "'> ";
					_html +=  dataJson[index].district ;
					_html += "</option> ";
		        });
				$("#gf-district").html(_html);
		    },
		    failure: function(data) { 
		        alert('Got an error dude');
		    }
		}); 
	}
	
	function loadGFVillage(_district){
		var _province = $('#gf-province').val();
		$.ajax({
		    url: '/referral_system/ajaxListGFVillage/',
		    data: { district : _district , province : _province },
		    type: 'post', // This is the default though, you don't actually need to always mention it
		    success: function(data) {
		    	dataJson = $.parseJSON(data);
		    	var _html = "<option value='0'>-- Select --</option>";
				$.each(dataJson, function(index) {
					_html += "<option onclick=\"loadGarment('" + dataJson[index].village + "')\" value='" + dataJson[index].village + "'> ";
					_html +=  dataJson[index].village ;
					_html += "</option> ";
		        });
				$("#gf-village").html(_html);
		    },
		    failure: function(data) { 
		        alert('Got an error dude');
		    }
		}); 
	}
	
	function loadGarment(_village){
		var _province = $('#gf-province').val();
		var _district = $('#gf-district').val();
		$.ajax({
		    url: '/referral_system/ajaxListGarment/',
		    data: { village : _village, province : _province, district : _district },
		    type: 'post', // This is the default though, you don't actually need to always mention it
		    success: function(data) {
		    	 dataJson = $.parseJSON(data);
		    	var _html = "<option value='0'>-- Select --</option>";
				$.each(dataJson, function(index) {
					_html += "<option onclick=\"selectGarment('" + dataJson[index].fields.quest_21 + "','" + dataJson[index].fields.quest_25 + "')\" value='" + dataJson[index].fields.quest_21 + "'> ";
					_html +=  dataJson[index].fields.quest_20 ;
					_html += "</option> ";
		        });
				$("#garment").html(_html);
		    },
		    failure: function(data) { 
		        alert('Got an error dude');
		    }
		}); 
	}
	
	function selectGarment(shortcode, gps) {
		$("#gf-gps").val(gps);
	}