$(document).ready(function(){
  $(".dropdown").hover(
      function() {
          $('.dropdown-menu', this).not('.in .dropdown-menu').stop(true,true).slideDown("400");
          $(this).toggleClass('open');
      },
      function() {
          $('.dropdown-menu', this).not('.in .dropdown-menu').stop(true,true).slideUp("400");
          $(this).toggleClass('open');
      }
  );

  function closeSearch() {
    var $form = $('.navbar-collapse form[role="search"].active')
  	$form.find('input').val('');
		$form.removeClass('active');
	}

	// Show Search if form is not active // event.preventDefault() is important, this prevents the form from submitting
	$(document).on('click', '.navbar-collapse form[role="search"]:not(.active) button[type="submit"]', function(event) {
		event.preventDefault();
		var $form = $(this).closest('form'),
			$input = $form.find('input');
		$form.addClass('active');
		$input.focus();
	});
	// ONLY FOR DEMO // Please use $('form').submit(function(event)) to track from submission
	// if your form is ajax remember to call `closeSearch()` to close the search container
	// $(document).on('click', '.navbar-collapse form[role="search"].active button[type="submit"]', function(event) {
	// 	event.preventDefault();
	// 	var $form = $(this).closest('form'),
	// 		$input = $form.find('input');
	// 	$('#showSearchTerm').text($input.val());
  //         closeSearch()
	// });

  $(window).on('message', function(evt) {
    var msg = evt.originalEvent.data;

    if( msg.messageType == 'SCORE' ){
      $.ajax({
        type: "POST",
        url: "/api/gameplay/",
        data: {
          score: msg.score,
          game_id: $("#gameframe").data("gameid"),
          csrfmiddlewaretoken: getCookie('csrftoken')
        },
        success: function(data){
          if(data == 'success'){
            console.log("score has been submitted");
          }
          else{
            console.log("something is wrong");
          }
        },
        dataType: 'text'
      });
    }
    else if( msg.messageType == 'SAVE' ){

      var gameStateScore = 0;
      if("score" in msg.gameState){
        gameStateScore = msg.gameState.score;
      }

      console.log('submitting state, the score: '+msg.gameState.score);
      $.ajax({
        type: "POST",
        url: "/api/gameplay/",
        data: {
          score: gameStateScore,
          state: JSON.stringify(msg.gameState),
          game_id: $("#gameframe").data("gameid"),
          csrfmiddlewaretoken: getCookie('csrftoken')
        },
        success: function(data){
          if(data == 'success'){
            console.log("state has been submitted");
          }
          else{
            console.log(data);
          }
        },
        dataType: 'text'
      });
    }
    else if( msg.messageType == 'LOAD_REQUEST' ){
      console.log('load request');
      $.get("/api/gameplay/?game_id="+$("#gameframe").data("gameid"), function(data){
        if($.isEmptyObject(data)){
          var msg = {
            'messageType': 'ERROR',
            'info':'no data'
          };
          console.log('sending error data');
          gameframe.contentWindow.postMessage(msg, '*');
        }
        else{
          gameframe = document.getElementById('gameframe');
          var msg = {
            'messageType': 'LOAD',
            'gameState': JSON.parse(data.state),
            'score':data.score
          };
          console.log(data);
          // console.log(data[data.length-1].state);
          gameframe.contentWindow.postMessage(msg, '*');
        }
      })
    }
    else if( msg.messageType == 'SETTING' ){
      $('#gameframe').css('height', msg.options.height).css('width', msg.options.width);
    }

  });

});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
