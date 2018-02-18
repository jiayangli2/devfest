function initialize()
{
    var mapProp = {
        center: new google.maps.LatLng(51.508742,-0.120850),
        zoom: 7,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    var map = new google.maps.Map(document.getElementById("googleMap"),mapProp);
}

function loadScript()
{
    var script = document.createElement("script");
    script.type = "text/javascript";
    script.src = "http://maps.googleapis.com/maps/api/js?key=AIzaSyCNYZrJGxuFs9wH_UtkRGHu1dlAvYC2y6Q&sensor=true&callback=initialize";
    document.body.appendChild(script);
}

window.onload = loadScript;