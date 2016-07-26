
var geocoder = null;
var map = null;
var direction;
var panel = document.getElementById('direction-panel');
var customerMarker = null;
var listeMarkers = _markers;
var markers = [];
var closest = [];
var map;
var address_icon = 'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png';

var address = "";

$(function($) {
    // Asynchronously Load the map API 
    var script = document.createElement('script');

    script.src = "//maps.googleapis.com/maps/api/js?key=AIzaSyChwOoz0ZXqQS6EAVcdngeb_17KMLW3eTM&sensor=false&callback=initialize&libraries=geometry,places";
    document.body.appendChild(script);
});

function initialize() {
	geocoder = new google.maps.Geocoder();
    
    var bounds = new google.maps.LatLngBounds();
    var mapOptions = {
        mapTypeId: 'roadmap'
    };
                    
    // Display a map on the page
    map = new google.maps.Map(document.getElementById("map_canvas"), mapOptions);
    map.setTilt(45);
        
    // Multiple Markers
                        
    // Info Window Content
    var infoWindowContent = _infoWindowContent;
        
    // Display multiple markers on a map
    var infoWindow = new google.maps.InfoWindow(), marker, i;
    
    // Loop through our array of markers & place each one on the map  
    for( i = 0; i < listeMarkers.length; i++ ) {
        var position = new google.maps.LatLng(listeMarkers[i][1], listeMarkers[i][2]);
        bounds.extend(position);
        marker = new google.maps.Marker({
            position: position,
            map: map,
            title: listeMarkers[i][0]
        });
        /*
        marker = new google.maps.Marker({
            position: pt,
            map: map,
            icon: locations[i][5],
            address: locations[i][2],
            title: locations[i][0],
            html: locations[i][0] + "<br>" + locations[i][2]
        });
        */
        markers.push(marker);
        
        // Allow each marker to have an info window    
        google.maps.event.addListener(marker, 'click', (function(marker, i) {
            return function() {
                infoWindow.setContent(infoWindowContent[i][0]);
                infoWindow.open(map, marker);
            }
        })(marker, i));

        // Automatically center the map fitting all markers on the screen
        map.fitBounds(bounds);
    }

    // Override our map zoom level once our fitBounds function runs (Make sure it only runs once)
    var boundsListener = google.maps.event.addListener((map), 'bounds_changed', function(event) {
        //this.setZoom(16);
        //google.maps.event.removeListener(boundsListener);
    });
    
    
    
}

function clearRouteAndFacility(){
	if (direction != null) {
		direction.setMap(null);
		direction = null;
	}
	$("#direction-panel").html(" ");
	$("#selected-panel").html(" ");
	$("#id_selected_facility").val("");
	$("#btn-itineraire").hide();
	direction = new google.maps.DirectionsRenderer({
        map   : map, 
        panel : panel 
    });
}

function codeAddress() {
	clearRouteAndFacility();
	
	// cr = client residence
	// gf = garment factory
	var search_type = $( "input:radio[name='searchtype']:checked" ).val();
	
	if(search_type == 'cr') {
		address = document.getElementById('street').value;
		address += " " + document.getElementById('village').value;
		address += " " + document.getElementById('commune').value;
		address += " " + document.getElementById('district').value;
		address += " " + document.getElementById('province').value;
	} else {
		address = document.getElementById('gf-gps').value;
	}
    
    geocoder.geocode({
        'address': address
    }, function (results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            map.setCenter(results[0].geometry.location);
            if (customerMarker) customerMarker.setMap(null);
            
            customerMarker = new google.maps.Marker({
                map: map,
                icon: address_icon,
                position: results[0].geometry.location
            });
            for (var i = 0; i < markers.length; i++) {
                markers[i].setMap(null);
            }
            var numResults = parseInt(document.getElementById('numberResults').value);
            closest = findClosestN(results[0].geometry.location, numResults);
            
            bounds_2 = new google.maps.LatLngBounds();
            bounds_2.extend(customerMarker.getPosition());
            
            var _closest_div = "";
            for (var i = 0; i < closest.length; i++) {
                closest[i].setMap(map);
                bounds_2.extend(closest[i].getPosition());
                
                
                var dist_km = Math.round(closest[i].distance / 1000).toFixed(2);
                
                //populate div
                _closest_div += "<li class='list-closest-marker' onclick='animateSpecificMarker(" + closest[i].distance+ ")'>" + closest[i].title + " </li>" ;
                //_closest_div += "<li class='list-closest-marker' onclick='animateSpecificMarker(" + closest[i].distance+ ")'>" + closest[i].title + " [" + dist_km +  "km ] </li>" ;
                
            }
            if(closest.length > 0) {
            	$("#closest-fac-div").html("<h6>Closest Facilities</h6><ol>" + _closest_div + "</ol>");
            }
            map.fitBounds(bounds_2);
            // map.setZoom(16);
        } else {
            alert('Geocode was not successful for the following reason: ' + status);
        }
    });
}

function findClosestN(pt, numberOfResults) {
    var closest = [];
    for (var i = 0; i < markers.length; i++) {
        markers[i].distance = google.maps.geometry.spherical.computeDistanceBetween(pt, markers[i].getPosition());
        markers[i].setMap(null);
        closest.push(markers[i]);
    }
    closest.sort(sortByDist);
    return closest.splice(0,numberOfResults);
}

function sortByDist(a, b) {
    return (a.distance - b.distance)
}

function animateSpecificMarker(_distance) {
	_index = 0 ;
	for (var i = 0; i < markers.length; i++) {
        if(markers[i].distance == _distance) {
        	markers[i].setAnimation(google.maps.Animation.BOUNCE);
        	_index = i ;
        } else {
        	markers[i].setAnimation(null);
        }
    }
	calculate(markers[_index].getPosition());
	displaySelectedFacility(_index);
	$("#btn-itineraire").show();
}

function calculate(_destination){
    origin      = customerMarker.getPosition(); // Le point départ
    destination = _destination; // Le point d'arrivé
    if(origin && destination){
        var request = {
            origin      : origin,
            destination : destination,
            travelMode  : google.maps.DirectionsTravelMode.WALKING // Type de transport
        }
        var directionsService = new google.maps.DirectionsService(); // Service de calcul d'itinéraire
        directionsService.route(request, function(response, status){ // Envoie de la requête pour calculer le parcours
            if(status == google.maps.DirectionsStatus.OK){
                direction.setDirections(response); // Trace l'itinéraire sur la carte et les différentes étapes du parcours
            }
        });
    } //http://code.google.com/intl/fr-FR/apis/maps/documentation/javascript/reference.html#DirectionsRequest
};

function displaySelectedFacility(_index){
	var _selectedMarker = listeMarkers[_index] ;
	var _html_selected = "";
	
	_html_selected += " <span class='round label warning'><h6>" + _selectedMarker[0] + " <br/>" + _selectedMarker[19] + "</h6></span>";
	_html_selected += "<h6>Address [EN]</h6>";
	_html_selected += "<p>" + _selectedMarker[3] + " ";
	_html_selected += "" + _selectedMarker[4] + " ";
	_html_selected += "" + _selectedMarker[5] + " ";
	_html_selected += "" + _selectedMarker[6] + " ";
	_html_selected += "" + _selectedMarker[7] + "</p> ";
	
	_html_selected += "<h6>Address [KHMER]</h6>";
	_html_selected += "<p>" + _selectedMarker[18] + " ";
	_html_selected += "" + _selectedMarker[17] + " ";
	_html_selected += "" + _selectedMarker[16] + " ";
	_html_selected += "" + _selectedMarker[15] + " ";
	_html_selected += "" + _selectedMarker[14] + "</p> ";
	
	_html_selected += "<h6>Contact Telephone</h6>";
	_html_selected += "<p>" + _selectedMarker[8] + "</p>";
	_html_selected += "<h6>Opening Hours</h6>";
	_html_selected += "<p>" + _selectedMarker[9] + "</p>";
	_html_selected += "<h6>Available Services</h6>";
	_html_selected += "<p><b>FP Services: </b>" + _selectedMarker[10] + "</p>";
	_html_selected += "<p><b>Safe abortion services: </b>" + _selectedMarker[11] + ", " + _selectedMarker[12] + "</p>";
	
	//alert(_selectedMarker[13]);
	$("#id_selected_facility").val(_selectedMarker[13]);
	$("#selected-panel").html(_html_selected);
	
}
