function loadDistrict(_province){
		$.ajax({
		    url: '/referral_system/ajaxListDistrict/',
		    data: { province : _province },
		    type: 'post', // This is the default though, you don't actually need to always mention it
		    success: function(data) {
		    	dataJson = $.parseJSON(data);
		    	var _html = "<option value='0'>-- Select --</option>";
				$.each(dataJson, function(index) {
					_html += "<option onclick=\"loadVillage('" + dataJson[index].district + "')\" value='" + dataJson[index].district + "'> ";
					_html +=  dataJson[index].district ;
					_html += "</option> ";
		        });
				$("#district").html(_html);
		    },
		    failure: function(data) { 
		        alert('Got an error dude');
		    }
		}); 
	}
	
	function loadVillage(_district){
		var _province = $('#province').val();
		$.ajax({
		    url: '/referral_system/ajaxListVillage/',
		    data: { district : _district, province : _province },
		    type: 'post', // This is the default though, you don't actually need to always mention it
		    success: function(data) {
		    	dataJson = $.parseJSON(data);
		    	var _html = "<option value='0'>-- Select --</option>";
				$.each(dataJson, function(index) {
					_html += "<option onclick=\"loadFacilities('" + dataJson[index].village + "')\" value='" + dataJson[index].village + "'> ";
					_html +=  dataJson[index].village ;
					_html += "</option> ";
		        });
				$("#village").html(_html);
		    },
		    failure: function(data) { 
		        alert('Got an error dude');
		    }
		}); 
	}
	
	function loadFacilities(_village){
		var _province = $('#province').val();
		var _district = $('#district').val();
		$.ajax({
		    url: '/referral_system/ajaxListFacilities/',
		    data: { village : _village, province : _province, district : _district  },
		    type: 'post', // This is the default though, you don't actually need to always mention it
		    success: function(data) {
		    	 dataJson = $.parseJSON(data);
		    	var _html = "<option value='0'>-- Select --</option>";
				$.each(dataJson, function(index) {
					_html += "<option onclick=\"selectFacility('" + dataJson[index].fields.quest_21 + "')\" value='" + dataJson[index].fields.quest_21 + "'> ";
					_html +=  dataJson[index].fields.quest_20 ;
					_html += "</option> ";
		        });
				$("#selected_facility").html(_html);
		    },
		    failure: function(data) { 
		        alert('Got an error dude');
		    }
		}); 
	}
	
	function selectFacility(_quest_21){
		$.ajax({
		    url: '/referral_system/ajaxSelectFacility/',
		    data: { quest_21 : _quest_21 },
		    type: 'post', // This is the default though, you don't actually need to always mention it
		    success: function(data) {
		    	
		    	data = data.split('====');
		    	
		    	var _html = "<div class='callout success'>";
		    	_html += "<h5>" + data[0] + "</h5>";
		    	_html += "<h6>Address</h6>";
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
		    	_html += "<p><b>FP Services: </b>" + data[9] + "</p>";
		    	_html += "<p><b>Safe abortion services: </b>" + data[10] + ", " + data[11] + "</p>";
		    	_html += "</div>";
				
				$("#selected-facility-div").html(_html);
		    },
		    failure: function(data) { 
		        alert('Got an error dude');
		    }
		}); 
	}