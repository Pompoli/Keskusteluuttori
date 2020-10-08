$ ->
  $(".submit").click ->
    $.post '',
      'speaker': JSON.stringify(SPEAKER)
      (data) ->
        window.location.href = '/'
  $("#name").change ->
    SPEAKER.name = $(this).val()
