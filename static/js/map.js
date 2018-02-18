function initialize()
{
  var mapProp = {
    center: new google.maps.LatLng(40.808349, -73.962162),
    zoom: 15,};
  var map = new google.maps.Map(document.getElementById("googleMap"), mapProp);

    $.getJSON("http://35.231.41.21:5000/events", function(data){
      markers = []
      data.forEach(function(entry) {
        var contentString = 
        '<div class="placecard">'+
        '<div class="card hovercard">'+
        '<div class="avatar">'+entry["host"]+'</div>'+
        '<div class="info">'+
        '<div class="desc">'+
        '<span><i class="glyphicon glyphicon-glass"></i></span>'+
        '<p>'+entry["message"]+'</p>'+
        '</div>'+
        '<div class="desc">'+
        '<span><i class="glyphicon glyphicon-map-marker"></i></span>'+
        '<p>'+entry["location"]+'</p>'+
        '</div>'+
        '<div class="desc">'+
        '<span><i class="glyphicon glyphicon-calendar"></i></span>'+
        '<p>'+entry["time"]+'</p>'+
        '</div>'+
        '</div>'+
        '<div class="attend">'+
        '<h3>Attendees</h3>'+
        '<div class="tags">'+
        '<a href=" " title="999-111-1234">YJ</a>'+
        '<a href=" " title="999-111-1234">BO</a>'+
        '<a href=" " title="999-111-1234">NP</a>'+
        '<a href=" " title="999-111-1234">YH</a>'+
        '</div>'+
        '</div>'+
        '<div class="join">'+
        '<button type="button" class="btn btn-success">JOIN</button>'+
        '</div>'+
        '</div>'+
        '</div>';

      let y1 = entry["get_location"].lat;
      let y2 = entry["get_location"].lng;
      // var mapProp = {
      // center: new google.maps.LatLng(entry["get_location"]["lat"], entry["get_location"]["lng"]),
      // zoom: 15,};
      
        markers.push({"location" : new google.maps.LatLng(parseFloat(y1), parseFloat(y2)), "content" : contentString});
      });
      var infowindow;

      for(var i=0;i<markers.length;i++){
        var marker = new google.maps.Marker({position: markers[i]["location"]});
        marker.setMap(map);

        infowindow = new google.maps.InfoWindow({content: markers[i]["content"]});

        google.maps.event.addListener(marker, 'click', function() {
          infowindow.open(map,marker);
        });
      };

    })

}

function loadScript()
{
  var script = document.createElement("script");
  script.type = "text/javascript";
  script.src = "http://maps.googleapis.com/maps/api/js?key=AIzaSyCNYZrJGxuFs9wH_UtkRGHu1dlAvYC2y6Q&sensor=true&callback=initialize";
  document.body.appendChild(script);
}

$(document).ready(function () {
  //Initialize tooltips
  $('.nav-tabs > li a[title]').tooltip();

  //Wizard
  $('a[data-toggle="tab"]').on('show.bs.tab', function (e) {

    var $target = $(e.target);

    if ($target.parent().hasClass('disabled')) {
      return false;
    }
  });

  $(".next-step").click(function (e) {

    var $active = $('.wizard .nav-tabs li.active');
    $active.next().removeClass('disabled');
    nextTab($active);

  });
  $(".prev-step").click(function (e) {

    var $active = $('.wizard .nav-tabs li.active');
    prevTab($active);

  });
});

function nextTab(elem) {
  $(elem).next().find('a[data-toggle="tab"]').click();
}
function prevTab(elem) {
  $(elem).prev().find('a[data-toggle="tab"]').click();
}

window.onload = loadScript;
