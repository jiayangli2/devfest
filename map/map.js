function myMap(markers) {
	var mapProp= {
    	center:new google.maps.LatLng(40.808349, -73.962162),
    	zoom:15,};
	var map=new google.maps.Map(document.getElementById("googleMap"),mapProp);
	
	var marker = new google.maps.Marker({position: mapProp.center});
	marker.setMap(map);
	var infowindow = new google.maps.InfoWindow({content:'Info'});
	google.maps.event.addListener(marker, 'click', function() {
	  infowindow.open(map,marker);
	  });
}
