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

  $('#list').click(function(event){event.preventDefault();$('#products .item').removeClass('grid-group-item');$('#products .item').addClass('list-group-item');});
  $('#grid').click(function(event){event.preventDefault();$('#products .item').removeClass('list-group-item');$('#products .item').addClass('grid-group-item');});

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
      console.log('submitting state');
      $.ajax({
        type: "POST",
        url: "/api/gameplay/",
        data: {
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
