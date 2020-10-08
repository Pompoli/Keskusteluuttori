WAIT_TIME=1500

$ ->
  take_turn(speaker1, speaker2,0)
  $(document).keyup (e) ->
    if e.which >= 49 && e.which <= 57
      numberpressed = e.which - 48
      $("#choicebox .bubble:nth-child("+numberpressed+")").removeClass('selected').trigger('click')
  $(document).keydown (e) ->
    if e.which >= 49 && e.which <= 57
      numberpressed = e.which - 48
      $("#choicebox .bubble:nth-child("+numberpressed+")").addClass('selected')
take_turn = (speaker,other,counter=0) ->
  counter = counter+1
  choicebox = $('#choicebox')
  if choicebox.hasClass 'speaker1'
    choicebox.addClass 'speaker2'
    choicebox.removeClass 'speaker1'
  else
    choicebox.addClass 'speaker1'
    choicebox.removeClass 'speaker2'
  if speaker.cpu
    $.get '/answer/',
      'speaker': speaker.pk,
      'lines': JSON.stringify lines.list
      (data) ->
        $('#bubbles').append data
        if counter < 5 and lines.list.length > 0
          callback = -> take_turn(other, speaker,counter)
          setTimeout callback, WAIT_TIME
  else
    $.get '/choices/',
      'speaker': speaker.pk,
      'lines': JSON.stringify lines.list
      (data) ->
        $("#choicebox").html data
        callback = ->
          $("#choicebox .bubble").removeClass("disabled")
        setTimeout callback, WAIT_TIME
        $("#choicebox .bubble").click ->
          if !($(this).hasClass 'disabled')
            $(this).addClass 'exit'
            message=$(this).data("message")
            line = $(this).data("line")
            $.get '/answer/',
              'message':message,
              'line':line
              (data) ->
                callback2 = ->
                  $('#bubbles').append data
                  $('#choicebox').html('')
                  callback3 = ->
                    take_turn(other, speaker,counter)
                  setTimeout callback3, WAIT_TIME
                setTimeout callback2, WAIT_TIME

            $("#choicebox .bubble").addClass("disabled")
            $("#choicebox .bubble").not(this).addClass("exit-still")
