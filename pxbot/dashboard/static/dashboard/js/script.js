$(document).ready(function(){

    $('.check-active').on('change', function(){
        var id = this.id;
        $('#'+id).val("True")
        $('#form-update-active').submit();
    });

    function callAutomation(){
        $.ajax({
            url: "automation/",
            type: "GET",
            data: {},
            success: function (data) {
                console.log(data);
            },
            error: function (data) {
                console.log(data);
            }
        });
    }

    function pad (str, max) {
        str = str.toString();
        return str.length < max ? pad("0" + str, max) : str;
    }

    function getCountdown(){
        initTime = new Date();
        initTime.setHours(1);
        initTime.setMinutes(0);
        initTime = new Date(initTime.toISOString()).getTime();

        var currentdate = new Date();
        currentdate.setHours(currentdate.getHours());
        currentdate = new Date(currentdate.toISOString()).getTime();


        var $h = $(initTime);
        for(var i = 1; i < 23; i++){
            $h = $h.add(initTime + (3600000 * i) );
            var t = initTime + (3600000 * i) ;
            if (t > currentdate) {
                return t;
            }
        }
    }

    var countDownDate = getCountdown();


    function runClock(){
            // Get today's date and time
          var now = new Date().getTime();

          // Find the distance between now and the count down date
          var distance = countDownDate - now;

          // Time calculations for days, hours, minutes and seconds
          var days = Math.floor(distance / (1000 * 60 * 60 * 24));
          var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
          var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
          var seconds = Math.floor((distance % (1000 * 60)) / 1000);

          // Display the result in the element with id="demo"
          $('#count-down').html(pad(hours,2) + ":" + pad(minutes,2) + ":" + pad(seconds,2));

          // If the count down is finished, write some text
          if (distance < 0) {
                countDownDate = getCountdown();
                callAutomation();
          }
    }

    setInterval(runClock, 1000);


});



