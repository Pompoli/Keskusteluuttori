const WAIT_TIME=1500;

$(function() {
  take_turn(speaker1, speaker2,0);
  $(document).keyup(function(e) {
    if ((e.which >= 49) && (e.which <= 57)) {
      const numberpressed = e.which - 48;
      return $("#choicebox .bubble:nth-child("+numberpressed+")").removeClass('selected').trigger('click');
    }
  });
  return $(document).keydown(function(e) {
    if ((e.which >= 49) && (e.which <= 57)) {
      const numberpressed = e.which - 48;
      return $("#choicebox .bubble:nth-child("+numberpressed+")").addClass('selected');
    }
  });
});
var take_turn = function(speaker,other,counter) {
  if (counter == null) { counter = 0; }
  counter = counter+1;
  const choicebox = $('#choicebox');
  if (choicebox.hasClass('speaker1')) {
    choicebox.addClass('speaker2');
    choicebox.removeClass('speaker1');
  } else {
    choicebox.addClass('speaker1');
    choicebox.removeClass('speaker2');
  }
  if (speaker.cpu) {
    return $.get('/answer/', {
      'speaker': speaker.pk,
      'lines': JSON.stringify(lines.list)
    },
      function(data) {
        $('#bubbles').append(data);
        if ((counter < 5) && (lines.list.length > 0)) {
          const callback = () => take_turn(other, speaker,counter);
          return setTimeout(callback, WAIT_TIME);
        }
    });
  } else {
    return $.get('/choices/', {
      'speaker': speaker.pk,
      'lines': JSON.stringify(lines.list)
    },
      function(data) {
        $("#choicebox").html(data);
        const callback = () => $("#choicebox .bubble").removeClass("disabled");
        setTimeout(callback, WAIT_TIME);
        return $("#choicebox .bubble").click(function() {
          if (!($(this).hasClass('disabled'))) {
            $(this).addClass('exit');
            const message=$(this).data("message");
            const line = $(this).data("line");
            $.get('/answer/', {
              'message':message,
              'line':line
            },
              function(data) {
                const callback2 = function() {
                  $('#bubbles').append(data);
                  $('#choicebox').html('');
                  const callback3 = () => take_turn(other, speaker,counter);
                  return setTimeout(callback3, WAIT_TIME);
                };
                return setTimeout(callback2, WAIT_TIME);
            });

            $("#choicebox .bubble").addClass("disabled");
            return $("#choicebox .bubble").not(this).addClass("exit-still");
          }
        });
    });
  }
};
